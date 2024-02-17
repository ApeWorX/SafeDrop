import boa  # type: ignore
import pytest


@pytest.fixture(scope="session")
def nft(project, owner, hack_details):
    contract = boa.load(
        project.Claim.source_path,
        f"ipfs://{abs(hash('boa.example.com'))}",
        *hack_details,
    )
    contract.eval(f"self.owner = {owner.address}")
    return contract
