import React,{useState} from "react";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom"

//componentes
import Inicio from "./components/Inicio";
import Editor from "./components/Editor";
import ReporteSimbolo from "./components/ReporteSimbolo";
import ReporteError from "./components/ReporteError";


import "./App.css";

function App() {

  const [editor,setEditor] = useState(false);
  const [simbolo,setSimbolo] = useState(false);
  const [error,setError] = useState(false);


    function estadoEditor(){
        setSimbolo(false);
        setError(false);
        setEditor(true);
    }

    function estadoSimbolo(){
      setEditor(false);
      setError(false);
      setSimbolo(true);
    }

    function estadoError(){
      setEditor(false);
      setSimbolo(false);
      setError(true);
    }

  return (
    <div>
        <nav className="navbar navbar-expand-lg bg-light">
      <div className="container-fluid">
        <a className="navbar-brand">
          OLC 2
        </a>
      <button
        className="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
      <span className="navbar-toggler-icon" />
      </button>
      <div className="collapse navbar-collapse" id="navbarNav">
        <div>
          <button 
          type="submit" 
          className="btn btn-primary" 
          onClick={estadoEditor}
          >
            Editor
          </button>
        </div>
        <div> </div>
        <div><button type="submit" class="btn btn-primary" onClick={estadoSimbolo} >Reporte Simbolos</button></div>
        <div></div>
        <button type="submit" class="btn btn-primary" onClick={estadoError}>Reporte Errores</button>
      </div>
    </div>
  </nav>

    <div>

                <div className="container py-5 h-10">
                       <div className="row d-flex justify-content-center align-items-center h-100">
                           <div className="col-12 col-md-8 col-lg-6 col-xl-12">
                               <div className="card bg-dark text-white" style={{borderRadius: '1rem'}}>
                                   <div className="card-body p-5 text-center">
                                       <div className="mb-md-5 mt-md-4 pb-5">
                                        {editor?<Editor/>
                                        :simbolo?<ReporteSimbolo/>
                                        :error?<ReporteError/>:<h1>Bienvenido</h1> 
                                                                            
                                        }
                                                 
                                        </div>
                                      
                               </div>
                           </div>
                       </div>
                   </div>
                </div>
    </div>

    </div>

  );
}

export default App;
