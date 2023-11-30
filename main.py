#Levi Alexander perez Elizondo
#Sistema difuso

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#Variables de entrada y salida
volumen = ctrl.Antecedent(np.arange(0, 301, 1), 'volumen');
clima = ctrl.Antecedent(np.arange(0, 51, 1), 'clima');
hora = ctrl.Antecedent(np.arange(6, 23, 1), 'hora');
tiempo_semaforo = ctrl.Consequent(np.arange(10, 61, 1), 'tiempo_semaforo');

#funciones de membresia
#volumenes

volumen['bajo'] = fuzz.trimf(volumen.universe, [0, 50, 100]);
volumen['medio'] = fuzz.trimf(volumen.universe, [50, 100, 150]);
volumen['alto'] = fuzz.trimf(volumen.universe, [100, 150, 300]);

#climas
clima['LLuvia_ligera'] = fuzz.trimf(clima.universe, [0, 10, 20]);
clima['lluvia_fuerte'] = fuzz.trimf(clima.universe, [10, 20, 50]);
clima['normal'] = fuzz.trimf(clima.universe, [20, 30, 50]);
clima['tormenta'] = fuzz.trimf(clima.universe, [40, 45, 50])
clima['soleado'] = fuzz.trimf(clima.universe, [0, 10, 20])

#horas
hora['mañana'] = fuzz.trimf(hora.universe, [6, 7, 8]);
hora['hora_pico'] = fuzz.trimf(hora.universe, [7, 8, 9]);
hora['tarde_noche'] = fuzz.trimf(hora.universe, [18, 20, 22]);
hora['noche'] = fuzz.trimf(hora.universe, [20, 21, 22])
hora['madrugada'] = fuzz.trimf(hora.universe, [0, 3, 6])

#tiempo del semaforo
tiempo_semaforo['corto'] = fuzz.trimf(tiempo_semaforo.universe, [10, 15, 20]);
tiempo_semaforo['medio'] = fuzz.trimf(tiempo_semaforo.universe, [15, 25, 35]);
tiempo_semaforo['largo'] = fuzz.trimf(tiempo_semaforo.universe, [30, 45, 60]);

#reglas difusas
regla1 = ctrl.Rule(volumen['bajo'] & clima['LLuvia_ligera'] & hora['mañana'], tiempo_semaforo['corto']);
regla2 = ctrl.Rule(volumen['medio'] & clima['normal'] & hora['hora_pico'], tiempo_semaforo['medio']);
regla3 = ctrl.Rule(volumen['alto'] & clima['lluvia_fuerte'] & hora['tarde_noche'], tiempo_semaforo['largo']);
regla4 = ctrl.Rule(volumen['medio'] & clima['LLuvia_ligera'] & hora['tarde_noche'], tiempo_semaforo['medio']);
regla5 = ctrl.Rule(volumen['alto'] & clima['tormenta'] & hora['noche'], tiempo_semaforo['largo'])
regla6 = ctrl.Rule(volumen['bajo'] & clima['soleado'] & hora['madrugada'], tiempo_semaforo['corto'])
regla7 = ctrl.Rule(volumen['medio'] & clima['lluvia_fuerte'] & hora['mañana'], tiempo_semaforo['medio'])

#regla default
regla_defecto = ctrl.Rule(antecedent=(volumen['bajo'] & clima['normal'] & hora['mañana']), consequent=tiempo_semaforo['medio'], label='regla_defecto');

## crear sistema de control difuso con regla de fallback
sistema_control = ctrl.ControlSystem(rules=[regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla_defecto]);
sistema = ctrl.ControlSystemSimulation(sistema_control);

#fuzzyficacion
sistema.input['volumen'] = 120;
sistema.input['clima'] = 45;
sistema.input['hora'] = 21;

#activar el sistema de control
sistema.compute();

#imprimir el resultado
volumen.view();
clima.view();
hora.view();
tiempo_semaforo.view(sim=sistema);
plt.show();

##imprimir el resultado de la fuzzificacion
print("Resultado de la defuzzificacion: ", sistema.output['tiempo_semaforo']);
