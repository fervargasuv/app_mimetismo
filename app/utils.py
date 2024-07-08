# import streamlit as st
# from pathlib import Path
# import numpy as np
# import plotly.graph_objects as go
# from processing import load_frames, detect_mimicry_with_shift
# import os


# def listar_participantes(experimento):
#     ruta_experimento = os.path.join('', experimento)
#     participantes = [os.path.join(ruta_experimento, d) for d in os.listdir(ruta_experimento) if os.path.isdir(os.path.join(ruta_experimento, d))]
#     return participantes

# def plot_mimetismo_timeline(mimetismo_intervals, total_frames):
#     # Crear una línea de tiempo inicializada a 0 (sin mimetismo)
#     timeline = np.zeros(total_frames)
    
#     # Marcar los intervalos de mimetismo con 1
#     for start, end in mimetismo_intervals:
#         timeline[start:end] = 1
    
#     # Crear gráfico de la línea de tiempo con Plotly
#     fig = go.Figure()
    
#     x = np.arange(len(timeline)) / 50  # Convertir frames a segundos
#     colors = ['green' if val == 1 else 'red' for val in timeline]
    
#     fig.add_trace(go.Scatter(
#         x=x, y=np.ones_like(x),
#         mode='markers',
#         marker=dict(color=colors, size=10),
#         hoverinfo='text',
#         text=[f'Mimetismo: {"Sí" if val == 1 else "No"}' for val in timeline]
#     ))
    
#     # Configurar el eje x con etiquetas de tiempo
#     fig.update_layout(
#         title="Línea de Tiempo de Mimetismo",
#         xaxis_title='Tiempo (segundos)',
#         yaxis=dict(showticklabels=False),
#         showlegend=False,
#         height=200,
#         margin=dict(l=20, r=20, t=20, b=20)
#     )
    
#     return fig

# def main():
#     st.title("Detección de Mimetismo en Videos")
#     st.write("Este es un ejemplo de aplicación de detección de mimetismo.")
    
#     # Seleccionar experimento
#     experiment_path = st.selectbox("Selecciona un experimento", ["experimento1", "experimento12"])
#     if experiment_path:
#         experiment_path = Path(f"./data/{experiment_path}")
#         participantes=listar_participantes(experiment_path)
#         participante_1=participantes[0]
#         participante_2=participantes[1]

#         datos_participante1=load_frames(participante_1)
#         datos_participante2=load_frames(participante_2)

#         st.write(len(datos_participante1["frames"]))
#         st.write(len(datos_participante2["frames"]))
#         # Procesar el experimento
#         results=detect_mimicry_with_shift(datos_participante1,datos_participante2)
        
#         st.write(results)

#         fig = plot_mimetismo_timeline(results, len(datos_participante1["frames"]))
        
#         # Mostrar el gráfico con Streamlit
#         st.plotly_chart(fig)


# if __name__ == "__main__":
#     main()


# def plot_mimetismo_timeline(mimetismo_intervals, total_frames):
#     # Crear una línea de tiempo inicializada a 0 (sin mimetismo)
#     timeline = np.zeros(total_frames)
    
#     # Marcar los intervalos de mimetismo con 1
#     for start, end,participantes in mimetismo_intervals:
#         if participantes == 1:
#             timeline[start:end] = 1
#         if participantes == 2:
#             timeline[start:end] = 2
#         if participantes == 3:
#             timeline[start:end] = 3
#         if participantes == 4:
#             timeline[start:end] = 4

#     # Crear gráfico de la línea de tiempo con Plotly
#     fig = go.Figure()
    
#     x = np.arange(len(timeline)) / 50  # Convertir frames a segundos
#     colors = ['green' if val == 1 else 'blue' if val == 2 else 'orange' if val == 3 else 'pink' if val == 4 else 'red' for val in timeline]

    
#     fig.add_trace(go.Scatter(
#         x=x, y=np.ones_like(x),
#         mode='markers',
#         marker=dict(color=colors, size=10),
#         hoverinfo='text',
#         text=[f'Participante {int(val)}' if val in [1, 2, 3, 4] else 'No Mimetismo' for val in timeline]
#     ))
    
#     # Configurar el eje x con etiquetas de tiempo
#     fig.update_layout(
#         title="Línea de Tiempo de Mimetismo",
#         xaxis_title='Tiempo (segundos)',
#         yaxis=dict(showticklabels=False),
#         showlegend=False,
#         height=200,
#         margin=dict(l=20, r=20, t=20, b=20)
#     )
    
#     return fig








# import streamlit as st
# from pathlib import Path
# import numpy as np
# import matplotlib.pyplot as plt
# from math import pi
# from processing import load_frames, detect_mimicry_with_shift
# import os

# def listar_participantes(experimento):
#     ruta_experimento = os.path.join('', experimento)
#     participantes = [os.path.join(ruta_experimento, d) for d in os.listdir(ruta_experimento) if os.path.isdir(os.path.join(ruta_experimento, d))]
#     return participantes

# def contar_mimetismo(resultados):
#     conteos = {p: [0, 0, 0, 0] for p in resultados.keys()}  # Inicializar conteos

#     for p in resultados:
#         for start, end, other in resultados[p]:
#             conteos[p][other-1] += 1  # Incrementar el conteo para el otro participante

#     return conteos

# def grafico_de_radar(conteos):
#     participantes = list(conteos.keys())
#     categorias = ['Participante 1', 'Participante 2', 'Participante 3', 'Participante 4']

#     N = len(categorias)
#     angles = [n / float(N) * 2 * pi for n in range(N)]
#     angles += angles[:1]  # Cerrar el círculo

#     fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

#     colors = ['b', 'r', 'g', 'y']
#     for i, participante in enumerate(participantes):
#         valores = conteos[participante]
#         valores += valores[:1]  # Cerrar el círculo
#         ax.plot(angles, valores, linewidth=2, linestyle='solid', label=f'Participante {i+1}', color=colors[i])
#         ax.fill(angles, valores, color=colors[i], alpha=0.25)

#     ax.set_xticks(angles[:-1])
#     ax.set_xticklabels(categorias)

#     plt.title('Mimetismo entre Participantes')
#     plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    
#     return fig

# def main():
#     experiment_path = st.selectbox("Selecciona un experimento", ["experimento1", "experimento12"])

#     if experiment_path:
#         experiment_path = Path(f"./data/{experiment_path}")
#         participantes = listar_participantes(experiment_path)

#         if len(participantes) >= 4:
#             datos = {}
#             for i, participante in enumerate(participantes[:4], start=1):
#                 datos[f"p{i}"] = load_frames(participante)
#             total_frames = len(datos["p1"]["frames"])
#             st.write(f"Total frames: {total_frames}")

#             resultados = {f'p{i}': [] for i in range(1, 5)}
#             for p1 in range(1, 5):
#                 for p2 in range(1, 5):
#                     if p1 != p2:
#                         detecciones = detect_mimicry_with_shift(datos[f"p{p1}"], datos[f"p{p2}"])
#                         if len(detecciones[0]) == 2:
#                             resultados[f'p{p1}'].extend([(start, end, p2) for (start, end) in detecciones])
#                         else:
#                             resultados[f'p{p1}'].extend([(start, end, p2) for (start, end, _, is_mimetismo) in detecciones if is_mimetismo])

#             # Contar los casos de mimetismo
#             conteos = contar_mimetismo(resultados)
#             st.write(conteos)

#             # Crear y mostrar el gráfico de radar
#             fig=grafico_de_radar(conteos)
#             st.pyplot(fig)

#         else:
#             st.write("Se necesitan al menos 4 participantes para esta visualización.")

# if __name__ == "__main__":
#     main()




# import streamlit as st
# from pathlib import Path
# import numpy as np
# import plotly.graph_objects as go
# from processing import load_frames, detect_mimicry_with_shift
# import os
# import matplotlib.pyplot as plt
# import pandas as pd



# def listar_participantes(experimento):
#     ruta_experimento = os.path.join('', experimento)
#     participantes = [os.path.join(ruta_experimento, d) for d in os.listdir(ruta_experimento) if os.path.isdir(os.path.join(ruta_experimento, d))]
#     return participantes

# # def plot_mimetismo_stacked_area(mimetismo_intervals, total_frames, participant_number):
# #     x = np.arange(total_frames) / 50  # Convertir frames a segundos
# #     y_data = {1: np.zeros(total_frames), 2: np.zeros(total_frames), 3: np.zeros(total_frames), 4: np.zeros(total_frames)}
    
# #     for start, end, other_participant in mimetismo_intervals:
# #         y_data[other_participant][start:end] = other_participant
    
# #     fig = go.Figure()
    
# #     # Stacking the areas
# #     fig.add_trace(go.Scatter(x=x, y=y_data[1], fill='tozeroy', name='Participante 1', mode='none', fillcolor='rgba(0, 255, 0, 0.5)'))
# #     fig.add_trace(go.Scatter(x=x, y=y_data[2], fill='tonexty', name='Participante 2', mode='none', fillcolor='rgba(0, 0, 255, 0.5)'))
# #     fig.add_trace(go.Scatter(x=x, y=y_data[3], fill='tonexty', name='Participante 3', mode='none', fillcolor='rgba(165, 42, 42, 0.5)'))
# #     fig.add_trace(go.Scatter(x=x, y=y_data[4], fill='tonexty', name='Participante 4', mode='none', fillcolor='rgba(255, 105, 180, 0.5)'))
    
# #     fig.update_layout(
# #         title=f"Línea de Tiempo de Mimetismo para Participante {participant_number}",
# #         xaxis_title='Tiempo (segundos)',
# #         yaxis=dict(
# #             tickvals=[0, 1, 2, 3, 4],
# #             ticktext=['No Mimetismo', 'Participante 1', 'Participante 2', 'Participante 3', 'Participante 4'],
# #             showgrid=False
# #         ),
# #         showlegend=True
# #     )
    
# #     st.plotly_chart(fig)

# # Función para generar el gráfico de áreas apiladas
# def plot_mimetismo_stacked_area(resultados, total_frames):
#     x = np.arange(total_frames)
#     colors = ['green', 'blue', 'brown', 'pink']
#     participants = len(resultados)
    
#     # Crear gráficos para cada participante
#     for p in range(1, participants + 1):
#         y_data = np.zeros((total_frames, participants))  # Matriz para almacenar las áreas de los participantes
        
#         # Rellenar los intervalos de mimetismo para el participante actual
#         for start, end, other_participant in resultados[f'p{p}']:
#             y_data[start:end, other_participant - 1] = other_participant  # Asignar el valor del participante al intervalo
        
#         # Crear el gráfico de áreas apiladas
#         fig = go.Figure()

#         # Agregar trazas para cada participante
#         for i in range(participants):
#             fig.add_trace(go.Scatter(
#                 x=x, 
#                 y=y_data[:, i] * (y_data[:, i] != 0),  # Asegurar que los valores sean 0 o el índice del participante
#                 mode='lines',
#                 line=dict(width=0.5, color=colors[i]),
#                 stackgroup='one',  # Stack traces on top of each other
#                 name=f'Participante {i + 1}'
#             ))

#         # Configurar el diseño del gráfico
#         fig.update_layout(
#             title=f'Mimetismo del Participante {p}',
#             xaxis_title='Frames',
#             yaxis=dict(
#                 tickvals=[1, 2, 3, 4],
#                 ticktext=['Participante 1', 'Participante 2', 'Participante 3', 'Participante 4'],
#                 range=[0.5, 4.5]  # Ajustar el rango del eje Y
#             ),
#             showlegend=True
#         )

#         # Mostrar el gráfico en Streamlit
#         st.plotly_chart(fig)

# def main():
#     # Seleccionar experimento
#     experiment_path = st.selectbox("Selecciona un experimento", ["experimento1", "experimento12"])
#     if experiment_path:
#         experiment_path = Path(f"./data/{experiment_path}")
#         participantes = listar_participantes(experiment_path)

#         if len(participantes) >= 4:
#             datos = {}
#             for i, participante in enumerate(participantes[:4], start=1):
#                 datos[f"p{i}"] = load_frames(participante)

#             total_frames = len(datos["p1"]["frames"])
#             st.write(f"Total frames: {total_frames}")
            
#             # resultados = {
#             # 'p1': [(10, 50, 2), (150, 200, 3), (150, 200, 4), (350, 400, 2)],
#             # 'p2': [(20, 70, 1), (120, 170, 3), (220, 270, 4), (320, 370, 1)],
#             # 'p3': [(30, 80, 1), (130, 180, 2), (230, 280, 4), (330, 380, 1)],
#             # 'p4': [(40, 90, 1), (140, 190, 2), (240, 290, 3), (340, 390, 1)]
#             #             }
           
           
#             resultados = {f'p{i}': [] for i in range(1, 5)}
            
#             for p1 in range(1, 5):
#                 for p2 in range(1, 5):
#                     if p1 != p2:
#                         detecciones = detect_mimicry_with_shift(datos[f"p{p1}"], datos[f"p{p2}"])
#                         if len(detecciones[0]) == 2:
#                             resultados[f'p{p1}'].extend([(start, end, p2) for (start, end) in detecciones])
#                         else:
#                             resultados[f'p{p1}'].extend([(start, end, p2) for (start, end, _, is_mimetismo) in detecciones if is_mimetismo])

#             plot_mimetismo_stacked_area(resultados, total_frames)
#             # for p in range(1, 5):
#             #     plot_mimetismo_stacked_area(resultados[f'p{p}'], total_frames, p)
#         else:
#             st.write("Se necesitan al menos 4 participantes para esta visualización.")

# if __name__ == "__main__":
#     main()