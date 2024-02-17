# @version 0.3.10

interface Claim:
    def mint(to: address) -> bool: nonpayable
    def setMinter(minter: address): nonpayable

CLAIM_BLUEPRINT: immutable(address)

owner: public(address)
merkle_root: public(bytes32)
claims: public(HashMap[String[128], address])

event ClaimCreated:
    claim_address: address

@external
def __init__(claim_blueprint: address, merkle_root: bytes32):
    self.owner = msg.sender
    CLAIM_BLUEPRINT = claim_blueprint
    self.merkle_root = merkle_root

@external
def setMerkleRoot(merkle_root: bytes32):
    assert msg.sender == self.owner
    self.merkle_root = merkle_root

@external
def createClaim(baseURI: String[56], name: String[128], symbol: String[128], description: String[1024]):
    assert self.claims[symbol] == empty(address)
    claim_address: address = create_from_blueprint(CLAIM_BLUEPRINT, baseURI, name, symbol, description, code_offset=3)
    log ClaimCreated(claim_address)
    self.claims[symbol] = claim_address

@external
def claim(amount: uint256, symbol: String[128], proof: DynArray[bytes32, 160], receiver: address=msg.sender):
    key: uint256 = convert(receiver, uint256)
    leaf_node: bytes32 = keccak256(convert(amount, bytes32))
    assert self._process_proof(leaf_node, key, proof) == self.merkle_root
    Claim(self.claims[symbol]).mint(receiver)

@internal
@pure
def _process_proof(leaf: bytes32, key: uint256, proof: DynArray[bytes32, 160]) -> bytes32:
    node: bytes32 = leaf
    target_bit: uint256 = 1
    for sibling in proof:
        if key & target_bit != 0:
            node = keccak256(concat(sibling, node))    
        else:
            node = keccak256(concat(node, sibling))
        
        target_bit <<= 1
    
    return node
