import pandas as pd
import numpy as np

# Configurar dados simulados
escolas = ['Escola A', 'Escola B', 'Escola C']
turmas = ['Turma 1', 'Turma 2', 'Turma 3']
nomes = [f'Estudante {i}' for i in range(1, 501)]

data = {
    'Nome da Escola': np.random.choice(escolas, 500),
    'Turma': np.random.choice(turmas, 500),
    'Nome': nomes,
    'ProficienciaLinguagens': np.random.randint(200, 800, 500),
    'ProficienciaMatematica': np.random.randint(200, 800, 500),
    'ProficienciaCH': np.random.randint(200, 800, 500),
    'ProficienciaCN': np.random.randint(200, 800, 500),
}

df = pd.DataFrame(data)
df.to_csv('dados_proficiencia.csv', index=False)
