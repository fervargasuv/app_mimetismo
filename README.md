# app_mimetismo

El archivo Main.py en la rama main corresponde al codigo de entrenamiento del modelo CNN-LSTM utilizado para entrenar con casos de mimetismos confirmados, los datos utilizados para este entrenamiento fueron:

1.- Landmarks faciales de los participantes

2.- Movimientos en eje X,Y,Z correspondientes al yaw,pitch y roll de los participantes

a estos datos se les aplico una estandarizacion para que el modelo pudiese trabajarlos de mejor manera, esto utilizando un max min scaler que considera los valores maximos y minimos de los landmarks y movimientos en los ejes , para dejar los valores entre el 0 y 1, despues de eso con los datos se genera una matriz, esta matriz tiene la siguiente forma [[x1p1,y1p1,x2p1,y2p1,...x49p1,y49p1,x1p2,y1p2,.....,x49p2,y49p2,yawp1,rollp1,pitchp1,yawp2,rollp2,pitchp2],....] considerar que en esta matriz cada caso es 1 frame de los videos, despues esta matriz se agrega a otra matriz para cada caso donde cada matriz tiene 200 frames, estos 200 frames se escojieron dado que existen 4 condiciones para detectar mimetismo (ver paper doi:10.1080/10447318.2020.1752474 donde se explican las 4 condiciones), y estas se miden en intervalos de 4 segundos, dado que los videos de sewa cada 50 frames es 1 segundo se define los 200 segundos por caso, con estos datos resultantes se obtiene una matriz del estilo (casos mimetismo y no mimetismo,200 frames de cada caso, total de caracteristicas + etiqueta de mimetismo o no) en el caso de la etiqueta de mimetismo o no se le asigna un 1 a los casos de mimetismo (extraidos de sewa) y un 0 a los casos de no mimetismo (provienen de los mismos videos donde hay mimetismo pero de momentos aleatorios que no correspondan a los casos de mimetismo).

para el modelo CNN-LSTM se combinan redes neuronales convolucionales (CNN) y redes LSTM para clasificar momentos de mimetismo en los videos. esto funciona de la siguiente manera:

primero se extraen las caracteristicas aplicando 3 capas principales:

Las capas Conv1D extraen características locales de las secuencias temporales de video.

Las capas Dropout ayudan a prevenir el sobreajuste al apagar aleatoriamente una fracción de las neuronas.

Las capas MaxPooling1D reducen la dimensionalidad de las características.

despues se pasa por una etapa de captura de dependencias temporales:

donde la capa LSTM captura las dependencias temporales en las secuencias, esto para analizar la dinamica del mimetismo.

despues se pasa a la clasificacion utilizando capas Dense del modelo que aplican la clasificacion final.


Se utilizo una validacion cruzada para evaluar los datos utilizando K-folds que divide los datos de entrenamiento en distintos subconjuntos y realiza una primera evaluacion (esto sin los datos de test solamente con los de entrenamiento) para ver como se comporta el modelo.

el mejor resultado estuvo cerca de un 70% de precision, con 774 epochs y un batch size de 128 (utilize un metodo randomico para evaluar con diferentes parametros). pero en su mayoria los resultados rondaban el 60% de precision.


Puntos a considerar , la eleccion de LSTM fue en base a que se utilizan secuencias temporales, la CNN se utilizo para mejorar el modelo, pero es posible que existan otros modelos que puedan permitir una mejor prediccion en los casos de mimetismo o que se adecuen a los datos utilizados, tambien hace falta considerar mas caracteristicas no verbales, como son movimientos de las personas (brazos,manos,cuerpo) y caractedisticas prosodicas del audio (tono de la voz, intensidad,etc) esto para lograr un analisis mas completo de cada participante en los experimentos, el por que no se utilizaron en esta etapa es dado que los datos entregados por [sewa](https://db.sewaproject.eu) no contemplan todas estas posibilidad y hay que realizar un reprocesamiento de los datos con distintas herramientas a las que se utilizaron como mediapipe para analizar las caras o movimientos, o herramientas que permitan obtener mas caracteristicas de audio, tambien existen transcripciones que permiten un analisis enfocado a lo verbal.

Porfavor igualmente revisar este paper que ve acerca de la deteccion de mimetismo (DOI: 10.1109/ACII.2013.27) donde utilizan LSTM y modelos de regresion , pero se basan en comportamientos no verbables en particular como sonrisa, enojo , etc, y en nuestro caso se busca una deteccion mas amplia considerando todos los aspectos de las personas, igualmente en ese paper se utilizo otra base de datos llamada MAHNOB (busque acceso a esa base de datos pero esta caida la pagina dado que es del 2013 aprox).

Los resultados obtenidos del modelo y aplicados en la app que se encuentra en la rama master de este repositorio, contienen la siguiente estructura de datos:

Resultados:
P1:[frame inicio,frame fin, participante al que le realiza mimetismo],....,total de episodios detectados.
P2:[frame inicio,frame fin, participante al que le realiza mimetismo],....,total de episodios detectados.
P3:[frame inicio,frame fin, participante al que le realiza mimetismo],....,total de episodios detectados.
P4:[frame inicio,frame fin, participante al que le realiza mimetismo],....,total de episodios detectados.

para despues pasarse a un grafico de areas apiladas (por el momento ya que es posible cambiar los graficos como a uno de lineas mostrado por profesor roberto o a uno de cuerdas cajas)

