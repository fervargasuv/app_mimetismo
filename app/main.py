import streamlit as st
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from processing import load_frames, detect_mimicry_with_shift
import os
import csv
import io
import zipfile
import tempfile

def listar_participantes(temp_dir):
    participantes = []
    for root, dirs, files in os.walk(temp_dir):
        if os.path.basename(root) == "experimento1":
            for dir_name in dirs:
                participantes.append(os.path.join(root, dir_name))
            break
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

def generar_csv(resultados):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Participante 1", "Inicio", "Fin", "Participante 2"])
    for p1 in range(1, 5):
        for (start, end, p2) in resultados[f'p{p1}']:
            writer.writerow([f'p{p1}', start, end, f'p{p2}'])
    return output.getvalue()

def main():
    st.title("Análisis de Mimetismo")
    uploaded_file = st.file_uploader("Sube un archivo ZIP con los datos de los participantes", type="zip")

    if uploaded_file:
        if 'datos' not in st.session_state:
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                participantes = listar_participantes(temp_dir)
                st.session_state.participantes = participantes
                st.write("Participantes encontrados:", participantes)

                datos = {}
                for i, participante in enumerate(participantes[:4], start=1):
                    datos[f"p{i}"] = load_frames(participante)
                    st.write(f"Datos del participante {i} cargados.")
                
                st.session_state.datos = datos
                st.session_state.total_frames = len(datos["p1"]["frames"])
                st.write(f"Total de frames: {st.session_state.total_frames}")

        datos = st.session_state.datos
        total_frames = st.session_state.total_frames
        participantes = st.session_state.participantes

        resultados = {f'p{i}': [] for i in range(1, 5)}
        for p1 in range(1, 5):
            for p2 in range(1, 5):
                if p1 != p2:
                    detecciones = detect_mimicry_with_shift(datos[f"p{p1}"], datos[f"p{p2}"])
                    if len(detecciones[0]) == 2:
                        resultados[f'p{p1}'].extend([(start, end, p2) for (start, end) in detecciones])
                    else:
                        resultados[f'p{p1}'].extend([(start, end, p2) for (start, end, _, is_mimetismo) in detecciones if is_mimetismo])
        
        plot_mimetismo_stacked_area(resultados, total_frames)
        
        csv_data = generar_csv(resultados)
        st.download_button(label="Descargar resultados en CSV", data=csv_data, file_name="resultados_mimetismo.csv", mime="text/csv")

if __name__ == "__main__":
    main()
