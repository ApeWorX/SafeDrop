from hexbytes import HexBytes

CLAIM_AMOUNT = abs(hash("ape"))


def test_integration(claim_blueprint, hack_details, project, hacker, db, safe_drop, owner):
    # Create a claim contract.
    base_uri = f"ipfs://{abs(hash('ape.example.com'))}"
    tx = safe_drop.createClaim(base_uri, *hack_details, sender=owner)
    nft = project.Claim.at(tx.events[0].claim_address)
    assert nft.baseURI() == base_uri
    assert nft.name() == hack_details[0]
    assert nft.symbol() == hack_details[1]
    assert nft.description() == hack_details[2]
    assert safe_drop.claims(nft.symbol()) == nft.address

    # Add someone able to claim.
    db.add({hacker.address: CLAIM_AMOUNT})
    safe_drop.setMerkleRoot(db.root, sender=owner)

    # Generate the proof needed to validate their claim.
    proof = db.proove(hacker.address)
    proof = [HexBytes(p) for p in list(reversed(proof))]

    # Expected values:
    expected_transfer = nft.Transfer(tokenId=int(hacker.address, 16), receiver=hacker.address)

    # Claim the NFT!
    tx = safe_drop.claim(CLAIM_AMOUNT, nft.symbol(), proof, sender=hacker)

    assert not tx.failed
    assert tx.events == [expected_transfer]
