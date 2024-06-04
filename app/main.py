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


def main():
    st.title("Detección de Mimetismo en Videos")
    st.write("Este es un ejemplo de aplicación de detección de mimetismo.")
    
    # Seleccionar experimento
    experiment_path = st.selectbox("Selecciona un experimento", ["experimento1", "experimento12"])
    if experiment_path:
        experiment_path = Path(f"./data/{experiment_path}")
        participantes=listar_participantes(experiment_path)
        participante_1=participantes[0]
        participante_2=participantes[1]

        datos_participante1=load_frames(participante_1)
        datos_participante2=load_frames(participante_2)

        st.write(len(datos_participante1["frames"]))
        st.write(len(datos_participante2["frames"]))
        # Procesar el experimento
        results=detect_mimicry_with_shift(datos_participante1,datos_participante2)
        
        st.write(results)
        # # Mostrar resultados
        # duration = len(frames1) / 6  # Suponiendo 50 fps (ajusta esto según la realidad de tus frames)
        # st.write("Duración del experimento:", duration, "segundos")
        
        # timeline = np.zeros(len(frames1))
        # for start1, end1, offset, is_mimetismo in results:
        #     if is_mimetismo:
        #         timeline[start1:end1] = 1
        
        # # Crear gráfico de la línea de tiempo con Plotly
        # fig = go.Figure()
        
        # x = np.arange(len(timeline)) / 50  # Convertir frames a segundos
        # colors = ['green' if val == 1 else 'red' for val in timeline]
        
        # fig.add_trace(go.Scatter(
        #     x=x, y=np.ones_like(x),
        #     mode='markers',
        #     marker=dict(color=colors, size=10),
        #     hoverinfo='text',
        #     text=[f'Mimetismo: {"Sí" if val == 1 else "No"}' for val in timeline]
        # ))
        
        # # Configurar el eje x con etiquetas de tiempo
        # fig.update_layout(
        #     xaxis_title='Tiempo (segundos)',
        #     yaxis=dict(showticklabels=False),
        #     showlegend=False,
        #     height=200,
        #     margin=dict(l=20, r=20, t=20, b=20)
        # )
        
        # st.plotly_chart(fig)

if __name__ == "__main__":
    main()
