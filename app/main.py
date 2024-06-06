import streamlit as st
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from processing import load_frames, detect_mimicry_with_shift
import os


def listar_participantes(experimento):
    ruta_experimento = os.path.join('', experimento)
    participantes = [os.path.join(ruta_experimento, d) for d in os.listdir(ruta_experimento) if os.path.isdir(os.path.join(ruta_experimento, d))]
    return participantes


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

def plot_mimetismo_timeline(mimetismo_intervals, total_frames, participant_number):
    timeline = np.zeros(total_frames)
    for start, end, other_participant in mimetismo_intervals:
        timeline[start:end] = other_participant

    colors = ['green' if val == 1 else 'blue' if val == 2 else 'brown' if val == 3 else 'pink' if val == 4 else 'red' for val in timeline]
    hover_texts = [f'Participante {int(val)}' if val in [1, 2, 3, 4] else 'No Mimetismo' for val in timeline]
    
    fig = go.Figure()
    x = np.arange(len(timeline)) / 50  # Convertir frames a segundos
    
    fig.add_trace(go.Scatter(
        x=x, y=np.ones_like(x),
        mode='markers',
        marker=dict(color=colors, size=10),
        hoverinfo='text',
        text=hover_texts
    ))
    
    fig.update_layout(
        title=f"Línea de Tiempo de Mimetismo para Participante {participant_number}",
        xaxis_title='Tiempo (segundos)',
        yaxis=dict(showticklabels=False),
        showlegend=False,
        height=200,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return fig

def main():
    # Seleccionar experimento
    experiment_path = st.selectbox("Selecciona un experimento", ["experimento1", "experimento12"])
    if experiment_path:
        experiment_path = Path(f"./data/{experiment_path}")
        participantes = listar_participantes(experiment_path)

        if len(participantes) >= 4:
            datos = {}
            for i, participante in enumerate(participantes[:4], start=1):
                datos[f"p{i}"] = load_frames(participante)

            total_frames = len(datos["p1"]["frames"])
            st.write(f"Total frames: {total_frames}")

            resultados = {f'p{i}': [] for i in range(1, 5)}
            
            for p1 in range(1, 5):
                for p2 in range(1, 5):
                    if p1 != p2:
                        detecciones = detect_mimicry_with_shift(datos[f"p{p1}"], datos[f"p{p2}"])
                        if len(detecciones[0]) == 2:
                            resultados[f'p{p1}'].extend([(start, end, p2) for (start, end) in detecciones])
                        else:
                            resultados[f'p{p1}'].extend([(start, end, p2) for (start, end, _, is_mimetismo) in detecciones if is_mimetismo])

            for p in range(1, 5):
                st.write(f"Resultados para participante {p}: {resultados[f'p{p}']}")
                fig = plot_mimetismo_timeline(resultados[f'p{p}'], total_frames, p)
                st.plotly_chart(fig)
        else:
            st.write("Se necesitan al menos 4 participantes para esta visualización.")

if __name__ == "__main__":
    main()
    
#[[P1]]