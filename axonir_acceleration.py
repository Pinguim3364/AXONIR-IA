"""
AXONIR Acceleration Wrapper
Loads compiled C++ library and exposes functions to Python
"""

import ctypes
import os
import platform
from typing import List, Optional
import subprocess
import tempfile

class AxonirAccelerationWrapper:
    """Wrapper para chamar C++ acceleration functions"""
    
    def __init__(self):
        self.lib = None
        self.available = False
        self._load_library()
    
    def _load_library(self):
        """Tenta carregar a biblioteca C++ compilada"""
        try:
            # Detecta plataforma
            system = platform.system()
            
            if system == "Linux":
                lib_name = "libaxonir_acceleration.so"
            elif system == "Darwin":  # macOS
                lib_name = "libaxonir_acceleration.dylib"
            elif system == "Windows":
                lib_name = "axonir_acceleration.dll"
            else:
                print(f"⚠️  Platform {system} not recognized")
                return
            
            # Procura em vários lugares
            possible_paths = [
                lib_name,
                f"./{lib_name}",
                f"./lib/{lib_name}",
                f"/usr/lib/{lib_name}",
                f"/usr/local/lib/{lib_name}",
                os.path.join(os.path.dirname(__file__), lib_name)
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        self.lib = ctypes.CDLL(path)
                        self.available = True
                        print(f"✅ C++ Acceleration library loaded from {path}")
                        return
                    except Exception as e:
                        print(f"⚠️  Failed to load {path}: {e}")
            
            print("⚠️  C++ Acceleration library not found")
            print(f"   Searched: {possible_paths}")
            print("   To compile: g++ -O3 -std=c++17 -pthread -fPIC -shared axonir_acceleration.cpp")
            
        except Exception as e:
            print(f"⚠️  Error loading C++ library: {e}")
    
    def is_available(self) -> bool:
        """Verifica se a biblioteca está disponível"""
        return self.available
    
    def parallel_sum(self, data: List[int]) -> int:
        """
        Soma paralela de array
        Usa multi-threading em CPU
        """
        if not self.available:
            print("⚠️  C++ Acceleration not available, falling back to Python")
            return sum(data)
        
        try:
            # Converte para C array
            arr = (ctypes.c_int * len(data))(*data)
            
            # Chama função C++
            self.lib.axonir_parallel_sum.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
            self.lib.axonir_parallel_sum.restype = ctypes.c_int
            
            result = self.lib.axonir_parallel_sum(arr, len(data))
            return result
        except Exception as e:
            print(f"⚠️  Error in parallel_sum: {e}")
            return sum(data)
    
    def parallel_sort(self, data: List[int]) -> List[int]:
        """
        Ordenação paralela
        Usa multi-threading
        """
        if not self.available:
            return sorted(data)
        
        try:
            arr = (ctypes.c_int * len(data))(*data)
            
            self.lib.axonir_parallel_sort.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
            self.lib.axonir_parallel_sort.restype = None
            
            self.lib.axonir_parallel_sort(arr, len(data))
            return list(arr)
        except Exception as e:
            print(f"⚠️  Error in parallel_sort: {e}")
            return sorted(data)
    
    def get_thread_count(self) -> int:
        """Retorna número de threads disponíveis"""
        if not self.available:
            import multiprocessing
            return multiprocessing.cpu_count()
        
        try:
            self.lib.axonir_get_thread_count.restype = ctypes.c_int
            return self.lib.axonir_get_thread_count()
        except:
            import multiprocessing
            return multiprocessing.cpu_count()
    
    def get_version(self) -> str:
        """Retorna versão da biblioteca"""
        if not self.available:
            return "AXONIR Acceleration (Python fallback)"
        
        try:
            self.lib.axonir_acceleration_version.restype = ctypes.c_char_p
            version = self.lib.axonir_acceleration_version()
            return version.decode('utf-8') if version else "Unknown"
        except:
            return "AXONIR Acceleration (C++ library loaded)"
    
    def get_info(self) -> str:
        """Retorna informações detalhadas"""
        if not self.available:
            return "AXONIR Acceleration (Python fallback - C++ library not available)"
        
        try:
            self.lib.axonir_acceleration_info.restype = ctypes.c_char_p
            info = self.lib.axonir_acceleration_info()
            return info.decode('utf-8') if info else "Unknown"
        except:
            return f"AXONIR Acceleration (C++ loaded, {self.get_thread_count()} threads)"


# ═══════════════════════════════════════════════════════════════════════════
# COMPILE C++ LIBRARY AUTOMATICALLY
# ═══════════════════════════════════════════════════════════════════════════

class AxonirCompiler:
    """Compila C++ automaticamente se necessário"""
    
    @staticmethod
    def compile():
        """Tenta compilar C++ automaticamente"""
        try:
            cpp_file = "axonir_acceleration.cpp"
            
            if not os.path.exists(cpp_file):
                print(f"⚠️  {cpp_file} not found, skipping compilation")
                return False
            
            system = platform.system()
            
            if system == "Windows":
                output = "axonir_acceleration.dll"
                cmd = f"g++ -O3 -std=c++17 -pthread -fPIC -shared {cpp_file} -o {output}"
            else:  # Linux/Mac
                output = "libaxonir_acceleration.so"
                cmd = f"g++ -O3 -std=c++17 -pthread -fPIC -shared {cpp_file} -o {output}"
            
            print(f"📦 Compiling C++ acceleration library...")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output):
                print(f"✅ Successfully compiled: {output}")
                return True
            else:
                print(f"⚠️  Compilation failed:")
                print(result.stderr)
                return False
        
        except Exception as e:
            print(f"⚠️  Could not compile C++: {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCE
# ═══════════════════════════════════════════════════════════════════════════

# Tenta compilar na primeira importação
AxonirCompiler.compile()

# Cria instância global
acceleration = AxonirAccelerationWrapper()


# ═══════════════════════════════════════════════════════════════════════════
# TESTES
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🛸 AXONIR Acceleration Test\n")
    
    print(f"Status: {'✅ Available' if acceleration.is_available() else '⚠️  Using Python fallback'}")
    print(f"Version: {acceleration.get_version()}")
    print(f"Info: {acceleration.get_info()}")
    print()
    
    # Test parallel sum
    data = list(range(1, 1001))  # 1 a 1000
    result = acceleration.parallel_sum(data)
    expected = sum(data)
    
    print(f"Parallel Sum Test:")
    print(f"  Input: list(1..1000)")
    print(f"  Result: {result}")
    print(f"  Expected: {expected}")
    print(f"  {'✅ PASS' if result == expected else '❌ FAIL'}")
    print()
    
    # Test parallel sort
    data = [5, 2, 8, 1, 9, 3, 7]
    result = acceleration.parallel_sort(data)
    expected = sorted(data)
    
    print(f"Parallel Sort Test:")
    print(f"  Input: {data}")
    print(f"  Result: {result}")
    print(f"  Expected: {expected}")
    print(f"  {'✅ PASS' if result == expected else '❌ FAIL'}")
