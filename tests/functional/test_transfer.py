import boa  # type: ignore


def test_mint(nft, owner, hacker):
    nft.setMinter(owner.address, sender=owner.address)
    nft.mint(hacker.address, sender=owner.address)

    # The token_id is the int-address of the receiver.
    expected_token_id = int(hacker.address, 16)
    assert nft.balanceOf(hacker.address) == 1
    assert nft.ownerOf(expected_token_id) == hacker.address


def test_mint_not_minter(nft, hacker, owner):
    """
    Hacker tries to mint their own without going
    through the minter.
    """
    nft.setMinter(owner.address, sender=owner.address)

    with boa.reverts():
        nft.mint(hacker.address, sender=hacker.address)
