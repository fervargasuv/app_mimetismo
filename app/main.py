import streamlit as st
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from processing import load_frames, detect_mimicry_with_shift
import os
import csv

def listar_participantes(experimento):
    ruta_experimento = os.path.join('', experimento)
    participantes = [os.path.join(ruta_experimento, d) for d in os.listdir(ruta_experimento) if os.path.isdir(os.path.join(ruta_experimento, d))]
    return participantes

def plot_mimetismo_stacked_area(resultados, total_frames):
    x = np.arange(total_frames)
    colors = ['green', 'blue', 'brown', 'pink']
    participants = len(resultados)

    for p in range(1, participants + 1):
        y_data = np.zeros((total_frames, participants))
        for start, end, other_participant in resultados[f'p{p}']:
            y_data[start:end, other_participant - 1] = other_participant

        fig = go.Figure()
        for i in range(participants):
            fig.add_trace(go.Scatter(x=x, y=y_data[:, i] * (y_data[:, i] != 0), mode='lines', line=dict(width=0.5, color=colors[i]), stackgroup='one', name=f'Participante {i + 1}'))

        fig.update_layout(
            title=f'Mimetismo del Participante {p}',
            xaxis_title='Frames',
            yaxis=dict(tickvals=[1, 2, 3, 4], ticktext=['Participante 1', 'Participante 2', 'Participante 3', 'Participante 4'], range=[0.5, 4.5]),
            showlegend=True
        )
        st.plotly_chart(fig)

def main():
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
            # Generar CSV con los resultados
            output_dir = "./resultados"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "resultados_mimetismo.csv")

            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Participante 1", "Inicio", "Fin", "Participante 2"])
                
                for p1 in range(1, 5):
                    for (start, end, p2) in resultados[f'p{p1}']:
                        writer.writerow([f'p{p1}', start, end, f'p{p2}'])
            
            plot_mimetismo_stacked_area(resultados, total_frames)
        else:
            st.write("Se necesitan al menos 4 participantes para esta visualización.")

if __name__ == "__main__":
    main()
