# Spanish version of the #93 page (draft translation, to be reviewed).
# P  : the docx blocks, keyed like the English ones (how1.., sum1.., s1p1.., s2b1.., ..., cover_sub). Plain text; the build escapes it.
# UI : every other text, keyed by the exact English text (or English inner html) it replaces.
# Numbers follow Spanish usage: decimal comma; no separator below 10 000 (4556), a dot above (44.440).

P = {
    'cover_sub': 'Ballenas, anguilas, ciclistas, robots, barcos y drones en una misma escala de energía',

    'how1': 'La vara de medir es el coste de transporte (COT): la energía que se gasta en mover un peso a lo largo de una distancia, dividida entre ese peso y esa distancia. No tiene unidades, así que una ballena, una bicicleta y un barco caben en el mismo eje. Un COT de 0,1 significa que mover 1 kg un metro cuesta tanta energía como subirlo 10 cm.',
    'how2': 'Dos bases, nunca mezcladas en una misma competición: «masa propia» (el animal, el robot o el vehículo completo que se mueve a sí mismo) y «carga transportada» (por kg de pasajero o de carga; un pasajero cuenta como 75 kg, la masa del conductor en la homologación de la UE).',
    'how3': 'Límite de la energía: los seres vivos y la fuerza humana se miden en energía de los alimentos (metabólica); las máquinas, en electricidad o combustible entregados al vehículo. No se cuentan en ningún caso la agricultura, las centrales eléctricas ni las refinerías.',
    'how4': 'Fuentes: todas las cifras son externas, y cada fuente figura con su URL al final de la página. Cuando una fuente da la energía y la masa pero no el COT, el COT se calcula y se muestran los datos de partida. No se estima nada; «ND» significa que no hay una cifra defendible.',

    'sum1': 'No existe un único medio más eficiente de moverse. Hay un ganador para cada cosa que decidas contar, y los ganadores comparten tres rasgos: son grandes, lentos y se apoyan en el agua, en raíles o en una carretera lisa.',
    'sum2': 'Entre los seres vivos ganan los grandes nadadores. Una ballena jorobada que cruza a su mejor velocidad tiene un coste de transporte de unos 0,0031, según una estimación a partir de la respiración; una anguila europea, medida en un túnel de natación, unos 0,060. Una persona que camina rápido gasta 0,387, unas 6 veces más que la anguila. El tamaño importa tanto como el medio: por kilogramo, un corredor del tamaño de un ratón gasta 47 veces más que uno del tamaño de un elefante.',
    'sum3': 'La bicicleta sigue siendo la mejor manera de que un cuerpo humano se mueva por sí mismo: 29 Wh de energía de los alimentos por km frente a 72 Wh al caminar. Pero las máquinas construidas solo para la eficiencia llegan mucho más lejos. Un prototipo de estudiantes en el Shell Eco-marathon de 2026 recorrió 538 km con 1 kWh: 1,9 Wh por km, un coste de 0,0091 por kg de conductor, unas 16 veces menos que un ciclista.',
    'sum4': 'En carga, el campeón es el barco: 0,014 por kg de mercancía, aproximadamente la mitad que un tren de mercancías y 1176 veces menos que un dron de reparto pequeño. Los robots son los rezagados: los mejores humanoides siguen gastando unas 10 veces más energía por metro que una persona que camina.',

    's1p1': 'Los ingenieros Gabrielli y von Karman se preguntaron en 1950 cuánto cuesta en energía la velocidad; el biólogo Vance Tucker respondió en 1975 con un gráfico que ponía en una misma línea moscas de la fruta, salmones, caballos, aviones a reacción y un hombre en bicicleta. Su truco fue dividir la energía entre el peso y la distancia, lo que elimina las unidades.',
    's1p2': 'Aquí se usa la misma fórmula para todas las filas. Muchas fuentes la publican directamente; para el resto se calcula a partir de la energía por kilómetro y la masa, o a partir de la potencia, la masa y la velocidad. Cada fila muestra sus datos de partida.',

    's2b1': 'Ballena jorobada: 0,0020-0,0042, derivado de la frecuencia respiratoria a la velocidad óptima de 2-4 m/s frente a Perú. Es el número más bajo de todo el análisis y el menos directo.',
    's2b2': 'Anguila europea: 0,051-0,069, medido en túneles de natación que simulan la migración de 5500 km hasta el mar de los Sargazos. Las anguilas nadan entre 4 y 6 veces más eficientemente que los peces de tipo salmón.',
    's2b3': 'Ballena beluga: 0,143, medido por consumo de oxígeno en un acuario.',
    's2b4': 'Medusa luna: se la cita como la nadadora más barata de su comparación, y solo los peces la superan por encima de unos 100 kg; su cuerpo es casi todo agua, lo que favorece a una métrica por kg. En el texto no se publica ningún número (ND).',
    's2b5': 'Aves: quienes vuelan se sitúan entre los nadadores y los corredores; el coste mínimo de un gorrión es unas diez veces menor que el de un ratón, porque recorre el terreno diez veces más rápido con la misma tasa metabólica. No se incluye ningún número comparable para aves.',
    's2p1': 'El tamaño importa tanto como el medio. Una regresión sobre 62 aves y mamíferos corredores da un coste neto de 3,76 para un corredor de 20 g, 0,285 para uno de 70 kg y 0,079 para uno de 4000 kg.',

    's3p1': 'En bicicleta, una persona necesita 29 Wh de energía de los alimentos por km, frente a unos 72 Wh a pie: bastante menos de la mitad. Aun así, los músculos pierden en forma de calor cerca de tres cuartas partes de la energía de los alimentos, y por eso un patinete eléctrico, con 15,9 Wh por km de electricidad, parece todavía más barato.',

    's4p1': 'El récord lo tiene el Cornell Ranger, que recorrió 65 km en 2011 con una sola carga a 0,280, cerca de una persona que camina, pero no sabe hacer nada más que caminar. El bípedo Cassie llega a 0,680. Los humanoides completos están en 2,27 (ASIMO) a 2,80 (WALK-MAN), diez o más veces una persona que camina, y el BigDog hidráulico en 15,0.',
    's4p2': 'La nueva generación de humanoides comerciales todavía no se puede situar en esta escala. El análisis comparativo de Fraunhofer IPA de 2026 sobre el Unitree G1 publica la duración de la batería (2 h 49 min de pie, 1 h 49 min de pie y caminando) pero no la distancia ni la velocidad, así que su coste de transporte es ND.',

    's5p1': 'En lo más alto, el prototipo del Eco-marathon (1,9 Wh por km) muestra el límite físico de un vehículo de una plaza sobre una pista lisa. Entre lo que la gente usa de verdad, lideran el patinete eléctrico compartido (15,9 Wh) y el autobús eléctrico lleno (unos 44 Wh por pasajero con 40 a bordo). Un coche eléctrico de batería con una sola persona gasta 210 Wh, y el pasajero-km medio de las carreteras británicas 395 Wh, unas 213 veces el prototipo.',

    's6p1': 'Un barco mueve una tonelada un kilómetro con unos 38 Wh, un tren de mercancías con 67 Wh, un camión medio con 608 Wh y un avión de carga con 4556 Wh. Un dron pequeño que lleva un paquete de 0,5 kg gasta 44.440 Wh por tonelada-km. Por paquete y en un trayecto corto aún puede superar a una furgoneta, pero por kilogramo es el medio más caro de todo el análisis.',
    's6p2': 'Visto como vehículo completo, un camión eléctrico de 40 toneladas en un modelo de diseño llega a 0,0098, una cifra cercana a la del barco por kg y más baja que la de cualquier animal terrestre.',

    's7b1': 'Si la pregunta es «¿qué ser vivo mueve su propio cuerpo de la forma más barata?»: los grandes nadadores. La ballena jorobada según la estimación (0,0020-0,0042); la anguila según la medición (0,051-0,069).',
    's7b2': 'Si es «¿qué forma de mover a una persona usa menos energía?»: un prototipo construido a propósito (0,0091 por kg de conductor). Entre las opciones cotidianas, el patinete eléctrico con electricidad y la bicicleta con energía de los alimentos.',
    's7b3': 'Si es «¿qué forma de mover mercancías usa menos energía?»: el barco (0,014 por kg de carga), y después el tren de mercancías.',
    's7b4': 'Si es «¿qué máquina camina como nosotros?»: ninguna todavía. El robot caminante más eficiente iguala a una persona solo porque no hace nada más.',

    's8b1': 'Pruebas comparativas de humanoides: Fraunhofer IPA ha publicado un método y no resultados; la primera distancia y velocidad publicadas de un humanoide comercial permitirán calcular un coste de transporte real.',
    's8b2': 'Camiones eléctricos y barcos: los escenarios de transporte eléctrico de larga distancia ya se sitúan en torno a tres veces el coste por kg del barco al mover carga; los datos de flotas lo pondrán a prueba.',
    's8b3': 'Vuelo de las aves: los estudios de marcado de aves en vuelo libre (por ejemplo, el proyecto FLIGHT de Swansea, con 46 especies) prometen los primeros costes de transporte comparables en campo para las aves.',
}

UI = {
    # ---- infographic and cover ----
    'Whale': 'Ballena', 'Eco car': 'Eco-coche', 'Ship': 'Barco', 'Eel': 'Anguila', 'Cyclist': 'Ciclista', 'Walker': 'Caminante', 'ASIMO': 'ASIMO', 'Drone': 'Dron',
    'COST OF TRANSPORT · LOG SCALE · LOWER IS BETTER': 'COSTE DE TRANSPORTE · ESCALA LOGARÍTMICA · MENOS ES MEJOR',
    'Eight movers on a rising curve of cost of transport, from the humpback whale at 0.003 to a delivery drone at 16': 'Ocho formas de moverse sobre una curva ascendente de coste de transporte, de la ballena jorobada con 0,003 a un dron de reparto con 16',
    'Language': 'Idioma',
    'The Cheapest Kilometre on Earth | Astara Intelligence In Depth #93': 'El kilómetro más barato de la Tierra | Astara Intelligence In Depth #93',
    'Row of glowing electric-vehicle fast chargers beside an old fuel station canopy at dusk, one car plugged in': 'Fila de cargadores rápidos iluminados para vehículos eléctricos junto a la marquesina de una vieja gasolinera al anochecer, con un coche enchufado',
    'Whales · Eels · Cyclists · Robots · Ships · Drones': 'Ballenas · Anguilas · Ciclistas · Robots · Barcos · Drones',
    'The cheapest<br>kilometre <span>on Earth</span>': 'El kilómetro<br>más barato <span>de la Tierra</span>',
    'Prepared 3 November 2026': 'Preparado el 3 de noviembre de 2026',
    'COT from 0.003 to 16': 'COT de 0,003 a 16',

    # ---- chapter titles and labels ----
    'There is no single <span>most efficient mover</span>': 'No existe un único <span>medio más eficiente</span>',
    'One number for <span>a whale and a ship</span>': 'Un solo número para <span>una ballena y un barco</span>',
    'Living beings: <span>big swimmers win</span>': 'Seres vivos: <span>ganan los grandes nadadores</span>',
    'The human body <span>and its best machine</span>': 'El cuerpo humano <span>y su mejor máquina</span>',
    'Robots: <span>still far from biology</span>': 'Robots: <span>aún lejos de la biología</span>',
    'Moving <span>people</span>': 'Mover <span>personas</span>',
    'Moving <span>goods</span>': 'Mover <span>mercancías</span>',
    'So, <span>who wins?</span>': 'Entonces, <span>¿quién gana?</span>',
    'What <span>to watch</span>': 'Qué <span>vigilar</span>',
    'Summary': 'Resumen', 'The Yardstick': 'La vara de medir', 'Living Beings': 'Seres vivos', 'The Human Body': 'El cuerpo humano', 'Robots': 'Robots',
    'Moving People': 'Personas', 'Moving Goods': 'Mercancías', 'The Verdict': 'El veredicto', 'What to Watch': 'Qué vigilar',

    # ---- figure titles and subtitles ----
    'Eight movers, one scale': 'Ocho formas de moverse, una sola escala',
    'Cost of transport, from the humpback whale (0.003) to a delivery drone (16). Log scale, lower is better.': 'Coste de transporte, de la ballena jorobada (0,003) a un dron de reparto (16). Escala logarítmica; cuanto menos, mejor.',
    'Lift a kilo by how much, for every metre you move it?': '¿Cuánto se eleva un kilo por cada metro que lo desplazas?',
    'Cost of transport read as a lift: a COT of 0.1 costs the energy of raising 1 kg by 10 cm for each metre travelled. Height on a log scale.': 'El coste de transporte visto como una elevación: un COT de 0,1 cuesta la energía de subir 1 kg 10 cm por cada metro recorrido. Altura en escala logarítmica.',
    'The champion of each class': 'El campeón de cada categoría',
    'One equation, no units': 'Una ecuación, sin unidades',
    'Cost of transport: the energy put in, divided by the weight moved and the distance': 'Coste de transporte: la energía aportada, dividida entre el peso movido y la distancia',
    'The scale runs across more than three orders of magnitude': 'La escala abarca más de tres órdenes de magnitud',
    'Every mover on one log axis, from the humpback whale (0.003) to the delivery drone (16)': 'Todos los medios en un solo eje logarítmico, de la ballena jorobada (0,003) al dron de reparto (16)',
    'The living podium': 'El podio de los seres vivos',
    'Cost of transport per kg of the animal itself, log scale. Lower is better.': 'Coste de transporte por kg del propio animal, escala logarítmica. Cuanto menos, mejor.',
    'Size matters as much as medium': 'El tamaño importa tanto como el medio',
    'Net cost of running against body mass, both on log scales: mouse to elephant': 'Coste neto de correr frente a la masa corporal, ambos en escala logarítmica: del ratón al elefante',
    'The bicycle more than halves the energy of walking': 'La bicicleta reduce a menos de la mitad la energía de caminar',
    'Walk, run, cycle: cost of transport and food energy per km': 'Caminar, correr, pedalear: coste de transporte y energía de los alimentos por km',
    'Humanoids still spend ten times more than a walking human': 'Los humanoides aún gastan diez veces más que una persona que camina',
    'Robots against two biological references, per kg of the machine, log scale': 'Robots frente a dos referencias biológicas, por kg de máquina, escala logarítmica',
    'A record prototype uses 1.9 Wh per person-km; the UK road average, 213 times more': 'Un prototipo récord usa 1,9 Wh por persona-km; la media de las carreteras del Reino Unido, 213 veces más',
    'Energy per person-km, sorted. Whiskers: car 1 to 4 occupants, double-decker 20 to 80 on board, and the spread across aircraft and Swedish city buses.': 'Energía por persona-km, ordenada. Bigotes: coche con 1 a 4 ocupantes, autobús de dos pisos con 20 a 80 a bordo, y la dispersión entre aviones y autobuses urbanos suecos.',
    'A ship moves a kilo about 1,176 times more cheaply than a drone': 'Un barco mueve un kilo unas 1176 veces más barato que un dron',
    'Energy per tonne-km of cargo, log scale': 'Energía por tonelada-km de carga, escala logarítmica',

    # ---- legends ----
    'Per kg of itself (own mass)': 'Por kg de sí mismo (masa propia)',
    'Per kg of passenger or cargo (payload)': 'Por kg de pasajero o de carga (carga transportada)',
    'Animals': 'Animales', 'Human body': 'Cuerpo humano', 'Range': 'Rango', 'Robot': 'Robot',
    'Human walking, net (0.22)': 'Persona que camina, neto (0,22)',
    'Horse, trotting (0.20)': 'Caballo al trote (0,20)',
    'Electricity, fuel or final energy': 'Electricidad, combustible o energía final',
    'Food energy (metabolic)': 'Energía de los alimentos (metabólica)',

    # ---- figure captions ----
    'An illustration, not a contest. Whale, eel, cyclist, walker and ASIMO are measured per kg of themselves; the Eco-marathon prototype, the ship and the drone per kg of passenger or cargo. Height follows the cost on a log scale; the horizontal order is by cost, not to scale.':
        'Una ilustración, no una competición. La ballena, la anguila, el ciclista, el caminante y ASIMO se miden por kg de sí mismos; el prototipo del Eco-marathon, el barco y el dron, por kg de pasajero o de carga. La altura sigue el coste en escala logarítmica; el orden horizontal es por coste, no a escala.',
    'An illustration, not a contest: the two bases are never ranked against each other. Whale, eel, cyclist (rider), walker and ASIMO are measured per kg of themselves; the Eco-marathon prototype, the ship and the drone per kg of passenger or cargo. COT = energy / (weight x distance). Lower is better.':
        'Una ilustración, no una competición: las dos bases nunca se comparan entre sí. La ballena, la anguila, el ciclista (el que pedalea), el caminante y ASIMO se miden por kg de sí mismos; el prototipo del Eco-marathon, el barco y el dron, por kg de pasajero o de carga. COT = energía / (peso x distancia). Cuanto menos, mejor.',
    'COT = energy / (weight x distance). Lower is better. Grades: A measured or official; B peer-reviewed model, synthesis or quoted review value; C manufacturer claim. The humpback whale value is derived from breathing, not from measured oxygen use.':
        'COT = energía / (peso x distancia). Cuanto menos, mejor. Grados: A, medido u oficial; B, modelo revisado por pares, síntesis o valor citado de una revisión; C, dato del fabricante. El valor de la ballena jorobada se deriva de la respiración, no de un consumo de oxígeno medido.',
    'Where a source gives energy and mass but not the cost of transport, the figure is computed from the inputs shown for each row. Oxygen is converted at 13.6 J per mg.':
        'Cuando una fuente da la energía y la masa pero no el coste de transporte, la cifra se calcula a partir de los datos de partida que muestra cada fila. El oxígeno se convierte a 13,6 J por mg.',
    'Bars show the range where a source gives one; the dot is the central value. Filled dots are per kg of the mover itself, hollow dots per kg of passenger or cargo: the two are never ranked against each other. Passenger figures use a 75 kg person (EU type-approval driver mass); real passengers and Eco-marathon drivers can be lighter, which would raise the per-kg values. <span id="v02-nd"></span>':
        'Las barras muestran el rango cuando una fuente lo da; el punto es el valor central. Los puntos rellenos son por kg del propio animal o vehículo, y los huecos por kg de pasajero o de carga: las dos bases nunca se comparan entre sí. Las cifras de pasajeros usan una persona de 75 kg (masa del conductor en la homologación de la UE); los pasajeros reales y los pilotos del Eco-marathon pueden pesar menos, lo que elevaría los valores por kg. <span id="v02-nd"></span>',
    'The humpback whale is the lowest number and the least direct: it is derived from breath counts and an assumed lung volume. Eel and beluga are measured oxygen use. The horse is a value quoted in a robotics review. Human rows are metabolic (food) energy: walking net of standing, walking fast (gross) and running. <span id="v04-nd"></span>':
        'La ballena jorobada es el número más bajo y el menos directo: se deriva del recuento de respiraciones y de un volumen pulmonar supuesto. La anguila y la beluga son consumo de oxígeno medido. El caballo es un valor citado en una revisión sobre robótica. Las filas humanas son energía metabólica (de los alimentos): caminar neto de estar de pie, caminar rápido (bruto) y correr. <span id="v04-nd"></span>',
    'A model line from one published regression across 62 running birds and mammals (Taylor, Heglund &amp; Maloiy 1982), not five measured animals. Net cost excludes the energy of standing still. Per kg, a mouse-sized runner spends about 47 times more than an elephant-sized one.':
        'Una línea de modelo a partir de una regresión publicada sobre 62 aves y mamíferos corredores (Taylor, Heglund &amp; Maloiy, 1982), no cinco animales medidos. El coste neto excluye la energía de estar de pie. Por kg, un corredor del tamaño de un ratón gasta unas 47 veces más que uno del tamaño de un elefante.',
    'Food energy, not electricity. Wh per km is food energy per person-km; for walking it is the incremental cost (range 56 to 88 Wh). ND: no defensible figure for that mode on the same basis. Muscles turn only about 22 to 25% of food energy into work.':
        'Energía de los alimentos, no electricidad. Los Wh por km son energía de los alimentos por persona-km; al caminar es el coste incremental (rango de 56 a 88 Wh). ND: no hay una cifra defendible para ese modo con la misma base. Los músculos convierten en trabajo solo entre el 22 y el 25 % de la energía de los alimentos.',
    'All robot figures are total electrical energy, except BigDog (fuel). Cassie is a preliminary experiment. The Unitree G1 cannot be placed: Fraunhofer IPA publishes battery life but no distance or speed, so its cost of transport is ND.':
        'Todas las cifras de robots son energía eléctrica total, salvo BigDog (combustible). Cassie es un experimento preliminar. El Unitree G1 no se puede situar: Fraunhofer IPA publica la duración de la batería pero no la distancia ni la velocidad, así que su coste de transporte es ND.',
    'Each bar keeps its energy boundary: do not read the bicycle and the e-scooter as like for like. The Eco-marathon prototype is a one-seat car built only to minimise energy on a closed track at low speed: a physics limit, not a usable vehicle. The Candela ferry is a manufacturer claim (grade C); the double-decker bus and the eVTOL are scenarios or design models. COT per kg of passenger uses 75 kg.':
        'Cada barra conserva su límite de energía: no se debe leer la bicicleta y el patinete eléctrico como equivalentes. El prototipo del Eco-marathon es un coche de una plaza construido solo para minimizar la energía en una pista cerrada y a baja velocidad: un límite físico, no un vehículo utilizable. El ferri Candela es un dato del fabricante (grado C); el autobús de dos pisos y el eVTOL son escenarios o modelos de diseño. El COT por kg de pasajero usa 75 kg.',
    'Per tonne of cargo carried. Whiskers: the 10th to 90th percentile for ship and train. The long-haul electric truck is a scenario estimate, not fleet data. <span id="v08-nd"></span>':
        'Por tonelada de carga transportada. Bigotes: del percentil 10 al 90 para el barco y el tren. El camión eléctrico de larga distancia es una estimación de escenario, no datos de flota. <span id="v08-nd"></span>',

    # ---- key figures ----
    'Per kg of itself, among living beings': 'Por kg de sí mismo, entre los seres vivos',
    'Per kg of itself, the best measured animal': 'Por kg de sí mismo, el mejor animal medido',
    'Per kg of person, human power': 'Por kg de persona, con fuerza humana',
    'Per kg of person, any machine': 'Por kg de persona, cualquier máquina',
    'Per kg of cargo': 'Por kg de carga',
    'Per kg of itself, legged robots': 'Por kg de sí mismo, robots con patas',
    'Humpback whale': 'Ballena jorobada', 'European eel': 'Anguila europea', 'Human on a bicycle': 'Persona en bicicleta',
    'Shell Eco-marathon prototype': 'Prototipo del Shell Eco-marathon', 'Ocean freight ship': 'Buque de carga oceánico',
    'Cornell Ranger (legged robot)': 'Cornell Ranger (robot con patas)',
    'own mass · Grade B': 'masa propia · Grado B', 'own mass (rider) · Grade B': 'masa propia (ciclista) · Grado B',
    'payload · Grade B': 'carga transportada · Grado B', 'payload · Grade A': 'carga transportada · Grado A', 'own mass · Grade A': 'masa propia · Grado A',

    # ---- excerpt, tags, reading rules ----
    'There is a winner for each thing you choose to count': 'Hay un ganador para cada cosa que decidas contar',
    'From the analysis': 'Del análisis',
    'Living beings': 'Seres vivos', 'Moving a person': 'Mover a una persona', 'Moving goods': 'Mover mercancías', 'Walking robots': 'Robots que caminan',
    'Humanoids · Fraunhofer IPA': 'Humanoides · Fraunhofer IPA', 'Electric trucks and ships': 'Camiones eléctricos y barcos', 'Bird flight · FLIGHT project': 'Vuelo de las aves · proyecto FLIGHT',
    'Yardstick': 'Vara de medir', 'Two bases': 'Dos bases', 'Energy boundary': 'Límite de la energía', 'Sources': 'Fuentes',
    '27 sources · research cut-off 3 November 2026': '27 fuentes · cierre de la investigación: 3 de noviembre de 2026',

    # ---- footer ----
    'Astara Intelligence In Depth is a periodic analysis of the automotive and mobility sector for professionals navigating strategic uncertainty.':
        'Astara Intelligence In Depth es un análisis periódico del sector del automóvil y la movilidad para profesionales que afrontan la incertidumbre estratégica.',
    'Sources: peer-reviewed studies, national statistics, university and manufacturer releases (full list above). Cost of transport (COT) = energy put in / (mass x g x distance). Two bases are used and never ranked against each other: own mass (the animal, robot or whole vehicle) and payload (the passenger, counted as 75 kg, or the cargo). Living beings and human power are measured in food (metabolic) energy; machines in electricity or fuel delivered to the vehicle. Farming, power plants and refineries are not counted. ND means no defensible figure was found by the research cut-off; it never means zero, and nothing has been estimated. Prepared 3 November 2026; figures reflect published data as of that date and are subject to revision. This newsletter is produced for informational purposes only and does not constitute investment advice. © 2026 Astara Intelligence.':
        'Fuentes: estudios revisados por pares, estadísticas nacionales y publicaciones de universidades y fabricantes (lista completa arriba). Coste de transporte (COT) = energía aportada / (masa x g x distancia). Se usan dos bases que nunca se comparan entre sí: masa propia (el animal, el robot o el vehículo completo) y carga transportada (el pasajero, contado como 75 kg, o la carga). Los seres vivos y la fuerza humana se miden en energía de los alimentos (metabólica); las máquinas, en electricidad o combustible entregados al vehículo. No se cuentan la agricultura, las centrales eléctricas ni las refinerías. ND significa que no se encontró una cifra defendible antes del cierre de la investigación; nunca significa cero, y no se ha estimado nada. Preparado el 3 de noviembre de 2026; las cifras reflejan los datos publicados a esa fecha y pueden revisarse. Este boletín se elabora solo con fines informativos y no constituye asesoramiento de inversión. © 2026 Astara Intelligence.',

    # ---- charts (texts built in the browser) ----
    'Height by which each mover lifts 1 kg per metre travelled:': 'Altura a la que cada medio eleva 1 kg por metro recorrido:',
    'COT equals E divided by m times g times d': 'El COT es igual a E dividido entre m por g por d',
    'Worked example': 'Ejemplo resuelto',
    'Shell Eco-marathon prototype: 1 kWh (3.6 million J) for 538 km, one occupant counted as {m} kg.': 'Prototipo del Shell Eco-marathon: 1 kWh (3,6 millones de J) para 538 km, con un ocupante contado como {m} kg.',
    'Energy put in, in joules: food, electricity or fuel.': 'Energía aportada, en julios: alimentos, electricidad o combustible.',
    'The mass moved, in kg: the mover itself, or its passenger or cargo.': 'La masa movida, en kg: el propio animal o vehículo, o su pasajero o su carga.',
    'Gravity, {g} m/s².': 'Gravedad, {g} m/s².',
    'The distance travelled, in metres.': 'La distancia recorrida, en metros.',
    'Cost of transport of {n} movers on a log scale:': 'Coste de transporte de {n} medios en escala logarítmica:',
    'Filled: per kg of itself': 'Relleno: por kg de sí mismo',
    'Hollow: per kg of passenger or cargo': 'Hueco: por kg de pasajero o de carga',
    'No comparable number (ND):': 'Sin cifra comparable (ND):',
    'ND means no defensible figure was found; it never means zero.': 'ND significa que no se encontró una cifra defendible; nunca significa cero.',
    'Cost of transport of living beings:': 'Coste de transporte de los seres vivos:',
    '<b>Not charted (ND): moon jellyfish.</b> It is reported as the cheapest swimmer in its comparison, but the value appears only in a chart, and its body is mostly water, which flatters a per-kg metric.':
        '<b>No representada (ND): medusa luna.</b> Se la cita como la nadadora más barata de su comparación, pero el valor aparece solo en un gráfico, y su cuerpo es casi todo agua, lo que favorece a una métrica por kg.',
    'Net cost of running against body mass, model line:': 'Coste neto de correr frente a la masa corporal, línea de modelo:',
    'Body mass →': 'Masa corporal →',
    'Net cost of running, COT (log) →': 'Coste neto de correr, COT (log) →',
    'Wh per km of food energy': 'Wh por km de energía de los alimentos',
    'no Wh per km figure (ND)': 'sin cifra de Wh por km (ND)',
    'Cost of transport': 'Coste de transporte',
    'per kg of the person': 'por kg de la persona',
    'scale': 'escala',
    'Food energy per km, Wh': 'Energía de los alimentos por km, Wh',
    'Robot cost of transport:': 'Coste de transporte de los robots:',
    'References:': 'Referencias:',
    'human walking': 'persona que camina', 'horse trotting': 'caballo al trote',
    'Horse, trotting': 'Caballo al trote', 'Human walking, net': 'Persona que camina, neto',
    'no distance data': 'sin datos de distancia', 'cost of transport ND': 'coste de transporte ND',
    'Fraunhofer IPA, May 2026': 'Fraunhofer IPA, mayo de 2026',
    'Energy per person-km:': 'Energía por persona-km:',
    'Energy per tonne-km:': 'Energía por tonelada-km:',
    'Not charted (ND):': 'No representado (ND):',
    'It is a whole-vehicle value (COT {c} per kg of truck plus load) with no tonne-km figure.': 'Es un valor del vehículo completo (COT {c} por kg de camión más carga) y no tiene cifra por tonelada-km.',

    # ---- groups, rows and tags ----
    'Moving people': 'Mover personas',
    'Human walking, fast': 'Persona que camina, rápido', 'Human running': 'Persona corriendo',
    'Walking, fast': 'Caminar, rápido', '70 kg, ~6 km/h': '70 kg, ~6 km/h',
    'Walking, net of standing': 'Caminar, neto de estar de pie', '190 adults, 1.34 m/s': '190 adultos, 1,34 m/s',
    'Running': 'Correr', '~1 kcal per kg per km': '~1 kcal por kg y km',
    'Cycling': 'Pedalear', '~16 km/h, 62 kg rider': '~16 km/h, ciclista de 62 kg',
    'Mouse': 'Ratón', 'Dog': 'Perro', 'Human': 'Persona', 'Horse': 'Caballo', 'Elephant': 'Elefante',
    'electricity': 'electricidad', 'food energy': 'energía de los alimentos', 'final energy': 'energía final', 'fuel': 'combustible', 'operating energy': 'energía operativa',
    'total electrical': 'eléctrica total', 'estimated from breathing rate': 'estimada a partir de la respiración', 'measured oxygen use': 'consumo de oxígeno medido',
    'net (above standing)': 'neto (por encima de estar de pie)', 'gross': 'bruto',
    'derived from breathing': 'derivado de la respiración', 'physics limit': 'límite físico', 'manufacturer claim': 'dato del fabricante',
    'model line': 'línea de modelo', 'scenario / model': 'escenario / modelo',

    # ---- mover names ----
    'Battery-electric 40-tonne truck (whole vehicle)': 'Camión eléctrico de batería de 40 t (vehículo completo)',
    'Freight train': 'Tren de mercancías',
    'Battery-electric truck, long haul': 'Camión eléctrico de batería, larga distancia',
    'Shared e-scooter': 'Patinete eléctrico compartido',
    'Elephant-sized runner (4,000 kg)': 'Corredor del tamaño de un elefante (4000 kg)',
    'Beluga whale': 'Ballena beluga',
    'Human on a bicycle (food energy)': 'Persona en bicicleta (energía de los alimentos)',
    'Horse-sized runner (500 kg)': 'Corredor del tamaño de un caballo (500 kg)',
    'Electric double-decker bus, 40 on board': 'Autobús eléctrico de dos pisos, 40 a bordo',
    'Truck freight, mode average': 'Transporte de mercancías en camión, media',
    'Human-sized runner (70 kg)': 'Corredor del tamaño de una persona (70 kg)',
    'Human walking (food energy)': 'Persona que camina (energía de los alimentos)',
    'Human walking, fast walk': 'Persona que camina, a paso rápido',
    'Dog-sized runner (20 kg)': 'Corredor del tamaño de un perro (20 kg)',
    'Electric hydrofoil ferry (Candela P-12)': 'Ferri eléctrico de hidroalas (Candela P-12)',
    'MIT Cheetah (quadruped)': 'MIT Cheetah (cuadrúpedo)',
    'Passenger rail, Great Britain average': 'Ferrocarril de pasajeros, media de Gran Bretaña',
    'Cassie (bipedal robot)': 'Cassie (robot bípedo)',
    'Battery-electric car': 'Coche eléctrico de batería',
    'eVTOL air taxi, 2 of 4 seats': 'Taxi aéreo eVTOL, 2 de 4 plazas',
    'Passenger aircraft (combustion)': 'Avión de pasajeros (combustión)',
    'Freighter aircraft': 'Avión de carga',
    'Road passenger transport, UK average': 'Transporte de pasajeros por carretera, media del Reino Unido',
    'Honda ASIMO (humanoid)': 'Honda ASIMO (humanoide)',
    'Urban bus, Swedish cities': 'Autobús urbano, ciudades suecas',
    'WALK-MAN (humanoid)': 'WALK-MAN (humanoide)',
    'Mouse-sized runner (20 g)': 'Corredor del tamaño de un ratón (20 g)',
    'BigDog (hydraulic quadruped)': 'BigDog (cuadrúpedo hidráulico)',
    'Small delivery drone, 0.5 kg parcel': 'Dron de reparto pequeño, paquete de 0,5 kg',
    'Moon jellyfish': 'Medusa luna',
    'Unitree G1 (humanoid)': 'Unitree G1 (humanoide)',
}
