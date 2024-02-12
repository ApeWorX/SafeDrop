# SafeDrop

A convenient way to disburse whitehat funds

## Design Requirements

1. Anyone can create a new SafeDrop contract from a blueprint-based Factory deployer
2. The contract is initialized with the root of a sparse merkle tree mapping an address to a relative claim amount for that address, as well as the sum total of all the amounts in the tree
3. An affected User can mint an NFT using a merkle proof, and the NFT contains the User's relative claim amount
4. Anyone can add a new Claim of whitehatted funds of a specific token type to disburse
5. An NFT holder can claim their portion of any disbursement that has been added by Claim ID, only one time
6. NFTs are transferrable using the ERC-721 standard

## TODO

- [ ] Smart Contract Design
- [ ] Unit/Fuzz Testing (in Titanoboa)
- [ ] Integration Testing (in Ape)
- [ ] Script for creating Merkle tree from a dataframe
- [ ] Deployment Script
- [ ] Frontend development
