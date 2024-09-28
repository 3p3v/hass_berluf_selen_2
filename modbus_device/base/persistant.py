from typing import List

# %%
class Memory_persistant:
    def load(self) -> dict:
        raise NotImplementedError()
    
    def save_single(self, addr: int, val: int):
        raise NotImplementedError()
    
    def save(self, addr: int, vals: List[int]):
        raise NotImplementedError()

# %%
class Memory_persistant_factory:
    def create_persistant(self, subfile: str):
        raise NotImplementedError()

# %%
class Persistant_dummy(Memory_persistant):
    def __init__(self, mem: dict, subfile: str):
        self._mem: dict = mem
        self._subfile = subfile
        self._mem[self._subfile] = {}
    
    def load(self) -> dict:
        raise RuntimeError("Persitant not found!")
    
    def save_single(self, addr: int, val: int):
        self._mem[self._subfile][addr] = val
    
    def save(self, addr: int, vals: List[int]):
        for a, v in zip(range(addr, addr + len(vals)), vals):
            self._mem[self._subfile][a] = v
            
class Persistant_dummy_factory(Memory_persistant_factory):
    def __init__(self):
        self._mem: dict = {}
    
    def create_persistant(self, subfile: str):
        return Persistant_dummy(self._mem, subfile)