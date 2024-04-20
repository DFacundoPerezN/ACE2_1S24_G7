import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HeatmapGrid from 'react-heatmap-grid';
import Ventana from './ventana'; // Asumiendo que el nombre del archivo y el componente es Ventana con mayúscula inicial
import './App.css';

const obtenerDatosHabitacion = async (startDate, endDate, selectedHabitacion,set_habitacion_disponible_rango) => {
  try {
    // Realiza la solicitud GET al endpoint del backend con los parámetros de fecha y habitación seleccionada
    const response = await axios.get(`http://localhost:3001/${selectedHabitacion}rango`, {
      params: {
        startDate: startDate,
        endDate: endDate
      }



    });
    if (response.data.lenght===0){
      set_habitacion_disponible_rango("-vacia");
        
    }else{
      set_habitacion_disponible_rango("-ocupada");

    }
    return response.data; // Retorna los datos obtenidos
  } catch (error) {
    console.error('Error al obtener los datos de la habitación:', error);
    throw error; // Relanza el error para manejarlo en el componente
  }
};


function App() {
  const [habitacionData_buscar, setHabitacionData_buscar] = useState([]);
  const [habitacion1Data, setHabitacion1Data] = useState([]);
  const [habitacion2Data, setHabitacion2Data] = useState([]);
  const [habitacion3Data, setHabitacion3Data] = useState([]);
  const [habitacion4Data, setHabitacion4Data] = useState([]);
  const [habitacion5Data, setHabitacion5Data] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedHabitacion, setSelectedHabitacion] = useState('habitacion1'); // Por defecto, habitación 1
  const [habitacion_disponible, set_habitacionDisponible]= useState('');
  const [habitacion_disponible2, set_habitacionDisponible2]= useState('');
  const [habitacion_disponible3, set_habitacionDisponible3]= useState('');
  const [habitacion_disponible4, set_habitacionDisponible4]= useState('');
  const [habitacion_disponible5, set_habitacionDisponible5]= useState('');
  const [habitacion_disponible_rango, set_habitacion_disponible_rango]= useState('');


  useEffect(() => {
    const obtenerDatos = async () => {
      try {
        const response1 = await axios.get('http://localhost:3001/habitacion1');
        const response2 = await axios.get('http://localhost:3001/habitacion2');
        const response3 = await axios.get('http://localhost:3001/habitacion3');
        const response4 = await axios.get('http://localhost:3001/habitacion4');
        const response5 = await axios.get('http://localhost:3001/habitacion5');
        setHabitacion1Data(response1.data);
        setHabitacion2Data(response2.data);
        setHabitacion3Data(response3.data);
        setHabitacion4Data(response4.data);
        setHabitacion5Data(response5.data);
        console.log("====los datos de la habitacion3")
        console.log(response1.data);
        //comparar con un arreglo vacia
        if (response1.data=== undefined){
          console.log("esta vacia");
          set_habitacionDisponible("-vacia"); 
        }else{
          // console.log("no lo esta jijiij")
          console.log("gege");
          set_habitacionDisponible('-ocupada');
          // console.log(response3.lenght)
        }
        console.log("datos de la habitacion 2", response2.data.length)
        if(response2.data.length === 0){
          set_habitacionDisponible2("-vacia");
        }else{
          set_habitacionDisponible2('-ocupada');
        }
        if(response3.data.length === 0){
          set_habitacionDisponible3("-vacia");
        }else{
          set_habitacionDisponible3('-ocupada');
        }
        if(response4.data.length === 0){
          set_habitacionDisponible4("-vacia");
        }else{
          set_habitacionDisponible4('-Ocuapado');
        }
        if(response5.data.length === 0){
          set_habitacionDisponible5("-vacia");
        }else{
          set_habitacionDisponible5('-ocupada');
        }

      } catch (error) {
        console.error('Error al obtener los datos:', error);
      }
    };



    // Llama a la función para obtener datos al cargar la página
    obtenerDatos();

    // Establece un temporizador para actualizar los datos cada 10 segundos
    const interval = setInterval(() => {
      obtenerDatos();
    }, 10000);

    // Retorna una función de limpieza para detener el temporizador cuando el componente se desmonta
    return () => clearInterval(interval);
  }, []); 

  useEffect(() => {
    // Llama a la función para obtener los datos de la habitación al cargar la página o cuando cambia alguna de las dependencias
    obtenerDatosHabitacion(startDate, endDate, selectedHabitacion,set_habitacion_disponible_rango)
      .then(data => {
        setHabitacionData_buscar(data);
      })
      .catch(error => {
        // Maneja el error, si es necesario
      });
  }, [startDate, endDate, selectedHabitacion]); // Se ejecuta cuando startDate, endDate o selectedHabitacion cambian

  const handleSubmit = (event) => {
    event.preventDefault();
    // Llama a la función para obtener los datos de la habitación seleccionada con las fechas seleccionadas
    obtenerDatosHabitacion(startDate, endDate, selectedHabitacion)
      .then(data => {
        setHabitacionData_buscar(data);
      })
      .catch(error => {
        // Maneja el error, si es necesario
      });
  };

   // Se ejecuta solo al montar el componente
  // Función para calcular el porcentaje de registros para cada posición de una habitación
    const calcularPorcentaje = (habitacionData, posicion) => {
    const totalRegistros = habitacionData.length;
    const conteo = habitacionData.reduce((total, item) => total + parseInt(item[posicion]), 0);
    return (conteo / totalRegistros) * 100;
  };

  // Función para asignar colores basados en el porcentaje de registros para cada posición
  const asignarColor = (porcentaje) => {
    // Asignar colores basados en los rangos de porcentajes especificados
    if (porcentaje === 0 || undefined) {
      return 'green';
    }else if (porcentaje <= 10) {
      return 'lightgreen'; // 0-10%: verde claro
    } else if (porcentaje <= 20) {
      return 'yellow'; // 11-20%: amarillo
    } else if (porcentaje <= 40) {
      return 'orange'; // 21-40%: naranja
    } else if (porcentaje <= 60) {
      return 'red'; // 41-60%: rojo
    } else if (porcentaje <= 80) {
      return 'maroon'; // 61-80%: morado
    } else if (porcentaje <= 100){
      return 'purple'; // 81-100%: rojo oscuro
    }else {
      return 'green';
    }
    
  };

  // Estructurar los datos para la cuadrícula 6x6 de la habitación 1

  const buscar_habitacionData =[
    [
      calcularPorcentaje(habitacionData_buscar, 'posicion1'),
      calcularPorcentaje(habitacionData_buscar, 'posicion2'),
      calcularPorcentaje(habitacionData_buscar, 'posicion3'),
      calcularPorcentaje(habitacionData_buscar, 'posicion4')
    ],
    [
      calcularPorcentaje(habitacionData_buscar, 'posicion5'),
      calcularPorcentaje(habitacionData_buscar, 'posicion6'),
      calcularPorcentaje(habitacionData_buscar, 'posicion7'),
      calcularPorcentaje(habitacionData_buscar, 'posicion8')
    ],
    [
      calcularPorcentaje(habitacionData_buscar, 'posicion9'),
      calcularPorcentaje(habitacionData_buscar, 'posicion10'),
      calcularPorcentaje(habitacionData_buscar, 'posicion11'),
      calcularPorcentaje(habitacionData_buscar, 'posicion12')
    ],
    [
      calcularPorcentaje(habitacionData_buscar, 'posicion13'),
      calcularPorcentaje(habitacionData_buscar, 'posicion14'),
      calcularPorcentaje(habitacionData_buscar, 'posicion15'),
      calcularPorcentaje(habitacionData_buscar, 'posicion16')
    ]
  ]
  const dataHabitacion1 = [
    [
      calcularPorcentaje(habitacion1Data, 'posicion1'),
      calcularPorcentaje(habitacion1Data, 'posicion2'),
      calcularPorcentaje(habitacion1Data, 'posicion3'),
      calcularPorcentaje(habitacion1Data, 'posicion4')
    ],
    [
      calcularPorcentaje(habitacion1Data, 'posicion5'),
      calcularPorcentaje(habitacion1Data, 'posicion6'),
      calcularPorcentaje(habitacion1Data, 'posicion7'),
      calcularPorcentaje(habitacion1Data, 'posicion8')
    ],
    [
      calcularPorcentaje(habitacion1Data, 'posicion9'),
      calcularPorcentaje(habitacion1Data, 'posicion10'),
      calcularPorcentaje(habitacion1Data, 'posicion11'),
      calcularPorcentaje(habitacion1Data, 'posicion12')
    ],
    [
      calcularPorcentaje(habitacion1Data, 'posicion13'),
      calcularPorcentaje(habitacion1Data, 'posicion14'),
      calcularPorcentaje(habitacion1Data, 'posicion15'),
      calcularPorcentaje(habitacion1Data, 'posicion16')
    ]
  ];

  // Estructurar los datos para la cuadrícula 6x6 de la habitación 2
  const dataHabitacion2 = [
    [
      calcularPorcentaje(habitacion2Data, 'posicion1'),
      calcularPorcentaje(habitacion2Data, 'posicion2'),
      calcularPorcentaje(habitacion2Data, 'posicion3'),
      calcularPorcentaje(habitacion2Data, 'posicion4')
    ],
    [
      calcularPorcentaje(habitacion2Data, 'posicion5'),
      calcularPorcentaje(habitacion2Data, 'posicion6'),
      calcularPorcentaje(habitacion2Data, 'posicion7'),
      calcularPorcentaje(habitacion2Data, 'posicion8')
    ],
    [
      calcularPorcentaje(habitacion2Data, 'posicion9'),
      calcularPorcentaje(habitacion2Data, 'posicion10'),
      calcularPorcentaje(habitacion2Data, 'posicion11'),
      calcularPorcentaje(habitacion2Data, 'posicion12')
    ],
    [
      calcularPorcentaje(habitacion2Data, 'posicion13'),
      calcularPorcentaje(habitacion2Data, 'posicion14'),
      calcularPorcentaje(habitacion2Data, 'posicion15'),
      calcularPorcentaje(habitacion2Data, 'posicion16')
    ]
  ];
  const dataHabitacion3 = [
    [
      calcularPorcentaje(habitacion3Data, 'posicion1'),
      calcularPorcentaje(habitacion3Data, 'posicion2'),
      calcularPorcentaje(habitacion3Data, 'posicion3'),
      calcularPorcentaje(habitacion3Data, 'posicion4')
    ],
    [
      calcularPorcentaje(habitacion3Data, 'posicion5'),
      calcularPorcentaje(habitacion3Data, 'posicion6'),
      calcularPorcentaje(habitacion3Data, 'posicion7'),
      calcularPorcentaje(habitacion3Data, 'posicion8')
    ],
    [
      calcularPorcentaje(habitacion3Data, 'posicion9'),
      calcularPorcentaje(habitacion3Data, 'posicion10'),
      calcularPorcentaje(habitacion3Data, 'posicion11'),
      calcularPorcentaje(habitacion3Data, 'posicion12')
    ],
    [
      calcularPorcentaje(habitacion3Data, 'posicion13'),
      calcularPorcentaje(habitacion3Data, 'posicion14'),
      calcularPorcentaje(habitacion3Data, 'posicion15'),
      calcularPorcentaje(habitacion3Data, 'posicion16')
    ]
  ];
  const dataHabitacion4 = [
    [
      calcularPorcentaje(habitacion4Data, 'posicion1'),
      calcularPorcentaje(habitacion4Data, 'posicion2'),
      calcularPorcentaje(habitacion4Data, 'posicion3'),
      calcularPorcentaje(habitacion4Data, 'posicion4')
    ],
    [
      calcularPorcentaje(habitacion4Data, 'posicion5'),
      calcularPorcentaje(habitacion4Data, 'posicion6'),
      calcularPorcentaje(habitacion4Data, 'posicion7'),
      calcularPorcentaje(habitacion4Data, 'posicion8')
    ],
    [
      calcularPorcentaje(habitacion4Data, 'posicion9'),
      calcularPorcentaje(habitacion4Data, 'posicion10'),
      calcularPorcentaje(habitacion4Data, 'posicion11'),
      calcularPorcentaje(habitacion4Data, 'posicion12')
    ],
    [
      calcularPorcentaje(habitacion4Data, 'posicion13'),
      calcularPorcentaje(habitacion4Data, 'posicion14'),
      calcularPorcentaje(habitacion4Data, 'posicion15'),
      calcularPorcentaje(habitacion4Data, 'posicion16')
    ]
  ];
  const dataHabitacion5 = [
    [
      calcularPorcentaje(habitacion5Data, 'posicion1'),
      calcularPorcentaje(habitacion5Data, 'posicion2'),
      calcularPorcentaje(habitacion5Data, 'posicion3'),
      calcularPorcentaje(habitacion5Data, 'posicion4')
    ],
    [
      calcularPorcentaje(habitacion5Data, 'posicion5'),
      calcularPorcentaje(habitacion5Data, 'posicion6'),
      calcularPorcentaje(habitacion5Data, 'posicion7'),
      calcularPorcentaje(habitacion5Data, 'posicion8')
    ],
    [
      calcularPorcentaje(habitacion5Data, 'posicion9'),
      calcularPorcentaje(habitacion5Data, 'posicion10'),
      calcularPorcentaje(habitacion5Data, 'posicion11'),
      calcularPorcentaje(habitacion5Data, 'posicion12')
    ],
    [
      calcularPorcentaje(habitacion5Data, 'posicion13'),
      calcularPorcentaje(habitacion5Data, 'posicion14'),
      calcularPorcentaje(habitacion5Data, 'posicion15'),
      calcularPorcentaje(habitacion5Data, 'posicion16')
    ]
  ];
  return (
  


    <div className="App">
    <h1 className='h1'>Mapa de Calor de Habitaciones G6</h1>
      <div style={{ display: 'flex' }}>
        <div style={{ marginRight: '20px' }}>
          <h2  className='h1_c'>Habitación 1 {habitacion_disponible}</h2>
          {/* <h2 className='h1_c'>{habitacion_disponible}</h2> */}
          {/* <div style={{ width: '500px', height: '300px' }}> */}
            <HeatmapGrid
              data={dataHabitacion1}
              background="#ffffff" // Color de fondo para las celdas sin datos
              xLabels={['1', '2', '3', '4']} // Etiquetas de las columnas
              yLabels={['1', '2', '3', '4']} // Etiquetas de las filas
              cellStyle={(background, value, min, max, data, x, y) => ({
                background: asignarColor(value),
                fontSize: '0px',
                width: '100px', // Establece el ancho de la celda
                height: '90px', // Establece la altura de la celda
              })}
              cellRender={(value) => value && `${value.toFixed(2)}%`}
              xLabelWidth={15}
              yLabelWidth={15}
              square
              // height={65}
              // width={40}
            />
          {/* </div> */}
        </div>
        <div>
          <h2 className='h1_c'>Habitación 2 {habitacion_disponible2}</h2>
          {/* <h2 className='h1_c'>{habitacion_disponible2}</h2> */}
            <HeatmapGrid
              data={dataHabitacion2}
              background="#ffffff" // Color de fondo para las celdas sin datos
              xLabels={['1', '2', '3', '4']} // Etiquetas de las columnas
              yLabels={['1', '2', '3', '4']} // Etiquetas de las filas
              cellStyle={(background, value, min, max, data, x, y) => ({
                background: asignarColor(value),
                fontSize: '0px',
                width: '100px', // Establece el ancho de la celda
                height: '90px', // Establece la altura de la celda
              })}
              cellRender={(value) => value && `${value.toFixed(2)}%`}
              xLabelWidth={15}
              yLabelWidth={15}
            />
          </div>
      <div>
          <h2  className='h1_c'>Habitación 3 {habitacion_disponible3}</h2>
            <HeatmapGrid
              data={dataHabitacion3}
              background="#ffffff" // Color de fondo para las celdas sin datos
              xLabels={['1', '2', '3', '4']} // Etiquetas de las columnas
              yLabels={['1', '2', '3', '4']} // Etiquetas de las filas
              cellStyle={(background, value, min, max, data, x, y) => ({
                background: asignarColor(value),
                fontSize: '0px',
                width: '100px', // Establece el ancho de la celda
                height: '90px', // Establece la altura de la celda
              })}
              cellRender={(value) => value && `${value.toFixed(2)}%`}
              xLabelWidth={15}
              yLabelWidth={15}
            />
          </div>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center',marginRight: '40px' }}>
        
        <div>
          <h2  className='h1_c'>Habitación 4 {habitacion_disponible4}</h2>
            <HeatmapGrid
              data={dataHabitacion4}
              background="#ffffff" // Color de fondo para las celdas sin datos
              xLabels={['1', '2', '3', '4']} // Etiquetas de las columnas
              yLabels={['1', '2', '3', '4']} // Etiquetas de las filas
              cellStyle={(background, value, min, max, data, x, y) => ({
                background: asignarColor(value),
                fontSize: '0px',
                width: '100px', // Establece el ancho de la celda
                height: '90px', // Establece la altura de la celda
              })}
              cellRender={(value) => value && `${value.toFixed(2)}%`}
              xLabelWidth={15}
              yLabelWidth={15}
            />
          </div>
          <div>
          <h2  className='h1_c'>Habitación 5 {habitacion_disponible5}</h2>
            <HeatmapGrid
              data={dataHabitacion5}
              background="#ffffff" // Color de fondo para las celdas sin datos
              xLabels={['1', '2', '3', '4']} // Etiquetas de las columnas
              yLabels={['1', '2', '3', '4']} // Etiquetas de las filas
              cellStyle={(background, value, min, max, data, x, y) => ({
                background: asignarColor(value),
                fontSize: '0px',
                width: '100px', // Establece el ancho de la celda
                height: '90px', // Establece la altura de la celda
              })}
              cellRender={(value) => value && `${value.toFixed(2)}%`}
              xLabelWidth={15}
              yLabelWidth={15}
            />
            </div>
        </div>
      {/* aca es mapa de rangos */}
      <hr style={{ borderTop: '4px solid #ccc', margin: '50px 0'}} />

      <h1 className='h1'>Registros historicos</h1>

      <form onSubmit={handleSubmit} className="formulario-container">
      <div className="form-group">
        <label className="label-custom" htmlFor="startDate">Fecha de inicio:</label>
        <input className="input-custom" type="date" id="startDate" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
      </div>
      <div className="form-group">
        <label className="label-custom" htmlFor="endDate">Fecha de fin:</label>
        <input className='input-custom' type="date" id="endDate" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
      </div>
      <div className="form-group">
        <label className="label-custom" htmlFor="habitacion">Selecciona una habitación:</label>
        <select className="select" id="habitacion" value={selectedHabitacion} onChange={(e) => setSelectedHabitacion(e.target.value)}>
          <option value="habitacion1">Habitación 1</option>
          <option value="habitacion2">Habitación 2</option>
          <option value="habitacion3">Habitación 3</option>
          <option value="habitacion4">Habitación 4</option>
          <option value="habitacion5">Habitación 5</option>
          {/* Agrega más opciones para otras habitaciones si es necesario */}
        </select>
      </div>
    </form>
      <div>
        <h2 className='h1_c'>Mapa de Calor de la {selectedHabitacion} {set_habitacion_disponible_rango} </h2>
      <div style={{  display: 'flex', justifyContent: 'center'}}>
        <div style={{   width: '500px', height: '300px'} }>
      <HeatmapGrid

              data={buscar_habitacionData}
              background="#ffffff" // Color de fondo para las celdas sin datos
              xLabels={['1', '2', '3', '4']} // Etiquetas de las columnas
              // agregarle stilo a los labels
              yLabels={['1', '2', '3', '4']} // Etiquetas de las filas
              cellStyle={(background, value, min, max, data, x, y) => ({
                background: asignarColor(value),
                fontSize: '0px',
                width: '100px', // Establece el ancho de la celda
                height: '90px', // Establece la altura de la celda
                
              })}
              cellRender={(value) => value && `${value.toFixed(2)}%`}
              xLabelWidth={15}
              yLabelWidth={15}
      />
      </div>
      </div>
      </div>
      {/* <div style={{ width: '500px', height: '500px' }}>
        <HeatmapGrid
          data={habitacionData}
          background="#ffffff" // Color de fondo para las celdas sin datos
          xLabels={['1', '2', '3', '4']} // Etiquetas de las columnas
          yLabels={['1', '2', '3', '4']} // Etiquetas de las filas
          // Resto del código para configurar el mapa de calor...
        />
      </div> */}
            <hr style={{ borderTop: '4px solid #ccc', margin: '50px 0',borderColor: "white"}} />

      </div>


  );
}

export default App;
