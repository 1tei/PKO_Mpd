import time
import random
from Book_friends import generate_read_books, simulated_annealing

def run_test(n):
    # Nejauši izvēlētu distanču pievienošana
    distance_matrix = [[random.randint(10, 100) if i != j else 0 for j in range(n)] for i in range(n)]
    
    # Sākotnējo grāmatu inicializācija
    initial_books = list(range(n))
    
    # Papildina lasīto grāmatu sarakstu
    read_books = generate_read_books(n, initial_books)
    
    start_time = time.time()
    try:
        best_route, best_cost = simulated_annealing(n, distance_matrix, initial_books, read_books)
        end_time = time.time()
        print(f"Tests ar n={n}:")
        print("Labākais maršruts:", best_route)
        print("Maršruta cena:", best_cost)
        print("Izpildes laiks:", end_time - start_time, "sekundes\n")
    except Exception as e:
        print(f"Tests ar n={n}: {e}\n")

# Testi
if __name__ == "__main__":
    print("Testi...\n")
    for n in [5, 10, 15, 20, 25]:
        run_test(n)



# Hard coded testa piemērs izmantots salīdzināšanai

# # Lasītāju un grāmatu skaits
#     n = 8 
    
#     # Attāluma matrica starp katru lasītāju
#     distance_matrix = [
#             [0, 85, 75, 95, 60, 70, 80, 90],
#             [80, 0, 65, 40, 50, 75, 55, 85],
#             [70, 60, 0, 30, 45, 50, 80, 90],
#             [60, 40, 30, 0, 20, 30, 60, 70],
#             [50, 60, 55, 20, 0, 25, 45, 65],
#             [40, 75, 70, 30, 25, 0, 35, 50],
#             [30, 50, 80, 60, 45, 35, 0, 55],
#             [20, 85, 90, 70, 65, 50, 55, 0]
#     ]
    
#     # Sākotnējo grāmatu inicializācija
#     initial_books = [0, 1, 2, 3, 4, 5, 6, 7]