import pytest


@pytest.fixture(scope="session")
def claim_blueprint(owner, project):
    tx = owner.declare(project.Claim)
    return tx.contract_address


@pytest.fixture(scope="session")
def safe_drop(owner, project, claim_blueprint):
    return owner.deploy(project.SafeDrop, claim_blueprint, b"")
