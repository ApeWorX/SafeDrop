import json
from pathlib import Path
from typing import Any

from ape.types import AddressType
from ape.utils import ManagerAccessMixin
from eth_pydantic_types import HashBytes32
from hexbytes import HexBytes
from trie.constants import BLANK_NODE  # type: ignore
from trie.smt import SparseMerkleTree  # type: ignore


class DB(ManagerAccessMixin):
    KEY_SIZE: int = 20  # Address size

    def __init__(self, path: Path | None = None) -> None:
        if path and not path.suffix == ".json":
            raise ValueError("Expecting JSON file.")
        elif path:
            self.path = path
        else:
            self.path = Path.home() / ".safedrop" / "db.json"

    @property
    def root(self) -> str:
        tree = self.as_tree()
        return HexBytes(tree.root_hash).hex()

    def as_tree(self) -> SparseMerkleTree:
        if self.path.is_file():
            data = json.loads(self.path.read_text())
            return SparseMerkleTree.from_db(
                db={HexBytes(k): HexBytes(v) for k, v in data["db"].items()},
                root_hash=HexBytes(data["root_hash"]),
                key_size=self.KEY_SIZE,
            )
        else:
            return SparseMerkleTree(key_size=self.KEY_SIZE)

    def purge(self):
        self.path.unlink(missing_ok=True)

    def add(self, claims: dict[AddressType, int]):
        tree = self.as_tree()
        for address, claim in claims.items():
            claim256 = HashBytes32.__eth_pydantic_validate__(claim)
            tree.set(HexBytes(address), claim256)

        self.save(tree=tree)

    def remove(self, *addresses):
        tree = self.as_tree()
        for address in addresses:
            tree.delete(HexBytes(address))

        self.save(tree=tree)

    def save(self, tree: SparseMerkleTree | None):
        tree = tree or self.as_tree()
        db = {
            "db": {HexBytes(k).hex(): HexBytes(v).hex() for k, v in tree.db.items()},
            "root_hash": HexBytes(tree.root_hash).hex(),
        }
        self.path.unlink(missing_ok=True)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(db))

    def get(self, address: AddressType | str) -> Any | None:
        tree = self.as_tree()
        address = self.conversion_manager.convert(address, AddressType)
        try:
            return tree.get(HexBytes(address))
        except KeyError:
            return None

    def check(self, address: AddressType | str) -> bool:
        return self.get(address) != BLANK_NODE

    def proove(self, address: AddressType | str) -> tuple[str, ...]:
        tree = self.as_tree()
        address = self.conversion_manager.convert(address, AddressType)
        branch = tree.branch(HexBytes(address))
        return tuple(map(lambda x: HexBytes(x).hex(), branch))
