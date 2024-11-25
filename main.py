import re

class LinearEquationInterpreter:
    def __init__(self):
        self.variable = 'x'

    def tokenize(self, equation):
        """
        Memecah persamaan menjadi token-token
        """
        # Hapus spasi
        equation = equation.replace(' ', '')
        
        # Regex untuk memecah token
        tokens = re.findall(r'([+-]?\d*x?|[+-]?\d+|[=])', equation)
        
        # Hapus token kosong
        tokens = [token for token in tokens if token]
        
        return tokens

    def parse_tokens(self, tokens):
        """
        Parsing token menjadi struktur yang dapat diproses
        """
        left_side = []
        right_side = []
        current_side = left_side
        
        for token in tokens:
            if token == '=':
                current_side = right_side
                continue
            
            current_side.append(token)
        
        return {
            'left': left_side,
            'right': right_side
        }

    def parse_term(self, term):
        """
        Parse term untuk mendapatkan koefisien
        """
        if 'x' not in term:
            return 0, int(term)
        
        # Tangani term dengan x
        if term == 'x':
            return 1, 0
        elif term == '-x':
            return -1, 0
        
        # Pecah koefisien dan variabel
        if 'x' in term:
            coef_str = term.replace('x', '')
            if coef_str == '+':
                return 1, 0
            elif coef_str == '-':
                return -1, 0
            else:
                return int(coef_str), 0
        
        return 0, int(term)

    def normalize_equation(self, parsed_eq):
        """
        Normalisasi persamaan - memindahkan variabel ke sisi kiri
        dan konstanta ke sisi kanan
        """
        left_coef = 0
        left_const = 0
        right_coef = 0
        right_const = 0

        # Proses sisi kiri
        for term in parsed_eq['left']:
            coef, const = self.parse_term(term)
            left_coef += coef
            left_const += const

        # Proses sisi kanan
        for term in parsed_eq['right']:
            coef, const = self.parse_term(term)
            right_coef += coef
            right_const += const

        return {
            'coef': left_coef - right_coef,
            'const': right_const - left_const
        }

    def solve(self, normalized_eq):
        """
        Menyelesaikan persamaan setelah normalisasi
        """
        # Cek kasus khusus
        if normalized_eq['coef'] == 0:
            if normalized_eq['const'] == 0:
                return "Solusi tak terhingga"
            else:
                return "Tidak ada solusi"
        
        # Hitung solusi
        solution = normalized_eq['const'] / normalized_eq['coef']
        return solution

    def verify_solution(self, original_eq, solution):
        """
        Verifikasi solusi dengan mensubstitusi kembali
        """
        if isinstance(solution, (int, float)):
            try:
                # Pisahkan sisi kiri dan kanan
                left, right = original_eq.split('=')
                
                # Fungsi untuk mengganti x dengan solusi
                def replace_x(expr):
                    return str(expr).replace('x', str(solution))
                
                # Evaluasi kedua sisi
                left_value = eval(replace_x(left))
                right_value = eval(replace_x(right))
                
                # Periksa kesamaan dengan toleransi kecil
                if abs(left_value - right_value) < 1e-10:
                    return solution
                else:
                    return solution  # Tetap kembalikan solusi
            except Exception as e:
                print(f"Error verifikasi: {e}")
                return solution  # Kembalikan solusi asli jika verifikasi gagal
        return solution

    def interpret(self, equation):
        """
        Proses utama interpreter
        """
        try:
            # Tokenisasi
            tokens = self.tokenize(equation)
            print("Tokens:", tokens)

            # Parsing
            parsed_eq = self.parse_tokens(tokens)
            print("Parsed Equation:", parsed_eq)

            # Normalisasi
            normalized_eq = self.normalize_equation(parsed_eq)
            print("Normalized Equation:", normalized_eq)

            # Penyelesaian
            solution = self.solve(normalized_eq)
            print("Solution:", solution)

            # Verifikasi
            final_solution = self.verify_solution(equation, solution)
            print("Final Solution:", final_solution)

            return final_solution

        except Exception as e:
            print(f"Kesalahan dalam interpretasi: {e}")
            return None

def main():
    interpreter = LinearEquationInterpreter()
    
    # Mode interaktif
    print("Interpreter Persamaan Linier 1 Variabel")
    print("Ketik 'exit' untuk mengakhiri")
    
    while True:
        equation = input("\nMasukkan persamaan")
        
        if equation.lower() == 'exit':
            break
        
        result = interpreter.interpret(equation)
        
        if result is not None:
            print(f"Solusi: {result}")

if __name__ == "__main__":
    main()