import React,{useState} from "react";

import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-java";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools"

import "./Editor.css"

function Editor(){

    const [informacion,setInformacion] = useState("");
    const [consola,setConsola] = useState("");

    function handleInputChange (newValue){
       console.log("change",newValue);
       setInformacion(newValue)
    }

   
    

    const enviarCarga = async(event)=>{
        console.log("enviar datos")
        event.preventDefault();
        const res = await fetch('http://localhost:7000/interpretar',{
            method:'post',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                "code":informacion
            })
        })
        
        const data = await res.json();
        
        setConsola(data)
        
       
    }

  

        return(

        <div>
            <div id="div1" >
            <AceEditor
            placeholder="Area de código"
            mode="javascript"
            theme="monokai"
            name="blah2"
            onChange={handleInputChange}
            editorProps={{ $blockScrolling: true }}
            setOptions={{
                 enableBasicAutocompletion: false,
                 enableLiveAutocompletion: false,
                enableSnippets: true
                }}
            />      
            </div>

            <div id="div2">
            <AceEditor
            placeholder="Area de Consola"
            mode="javascript"
            theme="monokai"
            name="blah2"
            value={consola.consola}
            editorProps={{ $blockScrolling: true }}
            setOptions={{
                 enableBasicAutocompletion: false,
                 enableLiveAutocompletion: false,
                enableSnippets: true
                }}
            />      
            </div>  
            <button type="submit" class="btn btn-primary" id="btnAnalizar" onClick={enviarCarga} >Analizar</button>  
                 
            
        </div>
        )

}

export default Editor;