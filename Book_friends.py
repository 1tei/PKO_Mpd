import random
import math

# Palīgfunkcija, lai aprēķinātu kopējo maršrutu
def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    
    # Summē attālumus starp katru lasītāju pāri
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][route[0]] 
    return total_distance

# Palīgfunkcija, kas atrod tuvāko lasītāju, kas nav izlasījis grāmatu
def find_next_reader(current_reader, distance_matrix, read_books, assigned_books, visited):
    n = len(distance_matrix) 
    best_distance = float('inf')
    next_reader = -1
    
    # Meklējam tuvāko lasītāju, pārbaudot vai tas nav ticis apmeklēts un nav izlasījis grāmatu
    for i in range(n):
        if i not in visited and assigned_books[current_reader] not in read_books[i]:
            # Ja attālums ir mazāks par labāko attālumu, tad atjauno labākā attāluma vērtību un saglabā lasītāju
            if distance_matrix[current_reader][i] < best_distance:
                best_distance = distance_matrix[current_reader][i]
                next_reader = i
                
    return next_reader

# Simulated Annealing funkcija, lai optimizētu gan kurjera maršrutu gan grāmatu sadali
def simulated_annealing(n, distance_matrix, initial_books, read_books, initial_temp=1000, cooling_rate=0.995, stopping_temp=1):
    # Atļautais mēģinājumu skaits
    max_attempts = 100
    attempts = 0
    
    while attempts < max_attempts:
        # Sāk pārbaudi ar nejauši izvēlētu lasītāju
        current_route = [random.randint(0, n-1)]
        assigned_books = initial_books[:]
        visited = set(current_route)

        # Piešķir grāmatas un izveido maršrutu
        while len(visited) < n:
            current_reader = current_route[-1]
            next_reader = find_next_reader(current_reader, distance_matrix, read_books, assigned_books, visited)
            # Ja nevar atrast nākamo lasītāju, tad iet ārā
            if next_reader == -1:
                break
            current_route.append(next_reader)
            visited.add(next_reader)

        if len(visited) == n:
            break

        attempts += 1

    if len(visited) < n:
        raise Exception("Nav iespējams izveidot maršrutu starp lasītājiem.")
    
    # Cost funkcijas aprēķināšana, izmantojot attālumu starp lasītājiem
    current_cost = calculate_total_distance(current_route, distance_matrix)
    best_route = current_route[:]
    best_cost = current_cost
    
    # Temperatūras uzstādīšana
    temperature = initial_temp
    
    # SA algoritma cikli kamēr temperatūra nesasneidz apstāšanās vērtību
    while temperature > stopping_temp:
        # Izveido neighborhood funkciju, apmainot abus lasītājus ar vietām
        new_route = current_route[:]
        if len(new_route) > 1:
            # Nejauši izvēlās divus lasītājus
            i, j = random.sample(range(len(new_route)), 2)
            # Apmaina lasītājus, izveidojot jaunu neighborhood risinājumu
            new_route[i], new_route[j] = new_route[j], new_route[i]
        
            # Jāpārbauda vai maršruts ir derīgs un lasītāji saņēmuši grāmatas, kuras nav lasījuši
            valid = True
            for k in range(len(new_route) - 1):
                if assigned_books[new_route[k]] in read_books[new_route[k + 1]]:
                    valid = False
                    break
            
            # Izlaiž nederīgos neighborhood risinājumus
            if not valid:
                continue 
            
            new_cost = calculate_total_distance(new_route, distance_matrix)
            
            # Pārbauda vai jaunais maršruts ir labāks par veco
            delta_cost = new_cost - current_cost
            
            # Nepieciešams izmantot Boltzmann formulu, lai apskatītu sliktākus maršrutus un izbēgtu no lokālā minimuma
            if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temperature):
                current_route = new_route[:]
                current_cost = new_cost
                
                # Atjauno pašreizējo labāko maršrutu
                if new_cost < best_cost:
                    best_route = new_route[:]
                    best_cost = new_cost
        
        temperature *= cooling_rate
    
    # Atgriež labāko maršrutu un maršruta cenu
    return best_route, best_cost

# Palīgfunkcija, lai piešķirtu grāmatas lasītājiem
def generate_read_books(n, assigned_books):
    read_books = []
    
    for i in range(n):
        # Katrs lasītājs ir izlasījis sev piešķirto grāmatu
        read_set = {assigned_books[i]}
        
        # Nejauši izvēlas jaunu grāmatu
        additional_books_count = random.randint(0, n - 2)
        
        # Izveido sarakstu ar citām grāmatām
        while len(read_set) < additional_books_count + 1:
            book_to_add = random.randint(0, n - 1)
            if book_to_add != assigned_books[i]:
                read_set.add(book_to_add)
        
        read_books.append(read_set)
    
    return read_books