
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftORleftANDleftIGUALQUENOIGUALQUEMENORQUEMENORIQUEMAYORQUEMAYORIQUEleftMASMENOSleftDIVIDIDOPORMODULOleftASrightUMENOSNOTnonassocPTOABS AND AS BARRAS BOOL BREAK CADENA CAPACITY CARACTER CHAR CLONE COMA CONTAINS CONTINUE CORDER CORIZQ DDOSPT DECIMAL DIVIDIDO DOSPT ELSE ENTERO F64 FALSE FN FOR GUIONB I64 ID IF IGUAL IGUALQUE IN INSERT LEN LET LLAVEDER LLAVEIZQ LOOP MAIN MAS MATCH MAYORIQUE MAYORQUE MENORIQUE MENORQUE MENOS MODULO MUT NEW NOIGUALQUE NOT OR PARDER PARIZQ POR POW POWF PRINTLN PTCOMA PTO PUSH REMOVE RETURN SIGNOI SQRT STR STRING TOOWNED TOSTRING TRUE USIZE VEC VVEC WHILE WITH_CAPACITYinicio : instrucciones main instruccionesmain : FN MAIN PARIZQ PARDER LLAVEIZQ instrucciones LLAVEDERinstrucciones : instrucciones instruccioninstrucciones : instruccioninstrucciones : instruccion : imprimir\n                          | declaracionimprimir : PRINTLN NOT PARIZQ expresiones PARDER PTCOMAdeclaracion : LET MUT ID DOSPT tipo IGUAL expresion PTCOMAdeclaracion : LET MUT ID IGUAL expresion PTCOMAdeclaracion : LET ID DOSPT tipo IGUAL expresion PTCOMAdeclaracion : LET ID IGUAL expresion PTCOMAtipo : I64\n            | F64\n            | BOOL\n            | CHAR\n            | STRING\n            | USIZE\n     expresiones : expresiones COMA expresionexpresiones : expresionexpresion : ENTEROexpresion : DECIMALexpresion : TRUEexpresion : FALSEexpresion : tostring\n                | toownedtostring : expresion PTO TOSTRING PARIZQ PARDER toowned : expresion PTO TOOWNED PARIZQ PARDER expresion : CADENAexpresion : CARACTERexpresion : expresion MAS expresion\n                    | expresion MENOS expresion\n                    | expresion POR expresion\n                    | expresion DIVIDIDO expresion\n                    | expresion MODULO expresionexpresion : MENOS expresion %prec UMENOS\n                | NOT expresionexpresion : I64 DDOSPT POW PARIZQ expresion COMA expresion PARDER\n                | F64 DDOSPT POWF PARIZQ expresion COMA expresion PARDERexpresion : expresion IGUALQUE expresion\n            | expresion NOIGUALQUE expresion\n            | expresion MENORQUE expresion\n            | expresion MAYORQUE expresion\n            | expresion MENORIQUE expresion\n            | expresion MAYORIQUE expresion expresion : PARIZQ expresion PARDERexpresion : PARIZQ expresion AS tipo PARDERexpresion : nativas_fun nativas_fun : expresion PTO ABS PARIZQ PARDER\n                    | expresion PTO SQRT PARIZQ PARDERnativas_fun : expresion PTO CLONE PARIZQ PARDER'
    
_lr_action_items = {'FN':([0,2,3,4,5,9,70,74,95,107,117,],[-5,10,-4,-6,-7,-3,-12,-8,-10,-11,-9,]),'PRINTLN':([0,2,3,4,5,8,9,14,70,71,74,95,97,107,108,117,],[6,6,-4,-6,-7,6,-3,6,-12,6,-8,-10,6,-11,-2,-9,]),'LET':([0,2,3,4,5,8,9,14,70,71,74,95,97,107,108,117,],[7,7,-4,-6,-7,7,-3,7,-12,7,-8,-10,7,-11,-2,-9,]),'$end':([1,3,4,5,8,9,14,70,74,95,107,108,117,],[0,-4,-6,-7,-5,-3,-1,-12,-8,-10,-11,-2,-9,]),'LLAVEDER':([3,4,5,9,70,71,74,95,97,107,117,],[-4,-6,-7,-3,-12,-5,-8,-10,108,-11,-9,]),'NOT':([6,16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[11,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'MUT':([7,],[12,]),'ID':([7,12,],[13,17,]),'MAIN':([10,],[15,]),'PARIZQ':([11,15,16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,87,88,89,90,91,92,93,94,104,105,118,119,],[16,20,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,99,100,101,102,103,104,105,22,22,22,22,22,]),'DOSPT':([13,17,],[18,37,]),'IGUAL':([13,17,39,40,41,42,43,44,45,67,],[19,38,69,-13,-14,-15,-16,-17,-18,94,]),'ENTERO':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'DECIMAL':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'TRUE':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'FALSE':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'CADENA':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'CARACTER':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,]),'MENOS':([16,19,21,22,24,25,26,27,28,29,30,31,32,33,36,38,46,48,49,51,52,53,54,55,56,57,58,59,60,61,62,64,68,69,72,75,76,77,78,79,80,81,82,83,84,85,86,94,96,104,105,106,109,110,111,112,113,114,115,116,118,119,120,121,122,123,],[33,33,33,33,53,-21,-22,-23,-24,-25,-26,-29,-30,33,-48,33,53,-37,53,33,33,33,33,33,33,33,33,33,33,33,33,-36,53,33,-46,53,-31,-32,-33,-34,-35,53,53,53,53,53,53,33,53,33,33,53,-47,-27,-28,-49,-50,-51,53,53,33,33,53,53,-38,-39,]),'I64':([16,18,19,21,22,33,37,38,51,52,53,54,55,56,57,58,59,60,61,62,69,73,94,104,105,118,119,],[34,40,34,34,34,34,40,34,34,34,34,34,34,34,34,34,34,34,34,34,34,40,34,34,34,34,34,]),'F64':([16,18,19,21,22,33,37,38,51,52,53,54,55,56,57,58,59,60,61,62,69,73,94,104,105,118,119,],[35,41,35,35,35,35,41,35,35,35,35,35,35,35,35,35,35,35,35,35,35,41,35,35,35,35,35,]),'BOOL':([18,37,73,],[42,42,42,]),'CHAR':([18,37,73,],[43,43,43,]),'STRING':([18,37,73,],[44,44,44,]),'USIZE':([18,37,73,],[45,45,45,]),'PARDER':([20,23,24,25,26,27,28,29,30,31,32,36,40,41,42,43,44,45,48,49,64,72,75,76,77,78,79,80,81,82,83,84,85,86,98,99,100,101,102,103,109,110,111,112,113,114,120,121,122,123,],[47,50,-20,-21,-22,-23,-24,-25,-26,-29,-30,-48,-13,-14,-15,-16,-17,-18,-37,72,-36,-46,-19,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,109,110,111,112,113,114,-47,-27,-28,-49,-50,-51,122,123,-38,-39,]),'COMA':([23,24,25,26,27,28,29,30,31,32,36,48,64,72,75,76,77,78,79,80,81,82,83,84,85,86,109,110,111,112,113,114,115,116,122,123,],[51,-20,-21,-22,-23,-24,-25,-26,-29,-30,-48,-37,-36,-46,-19,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,-47,-27,-28,-49,-50,-51,118,119,-38,-39,]),'MAS':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[52,-21,-22,-23,-24,-25,-26,-29,-30,-48,52,-37,52,-36,52,-46,52,-31,-32,-33,-34,-35,52,52,52,52,52,52,52,52,-47,-27,-28,-49,-50,-51,52,52,52,52,-38,-39,]),'POR':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[54,-21,-22,-23,-24,-25,-26,-29,-30,-48,54,-37,54,-36,54,-46,54,54,54,-33,-34,-35,54,54,54,54,54,54,54,54,-47,-27,-28,-49,-50,-51,54,54,54,54,-38,-39,]),'DIVIDIDO':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[55,-21,-22,-23,-24,-25,-26,-29,-30,-48,55,-37,55,-36,55,-46,55,55,55,-33,-34,-35,55,55,55,55,55,55,55,55,-47,-27,-28,-49,-50,-51,55,55,55,55,-38,-39,]),'MODULO':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[56,-21,-22,-23,-24,-25,-26,-29,-30,-48,56,-37,56,-36,56,-46,56,56,56,-33,-34,-35,56,56,56,56,56,56,56,56,-47,-27,-28,-49,-50,-51,56,56,56,56,-38,-39,]),'IGUALQUE':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[57,-21,-22,-23,-24,-25,-26,-29,-30,-48,57,-37,57,-36,57,-46,57,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,57,57,-47,-27,-28,-49,-50,-51,57,57,57,57,-38,-39,]),'NOIGUALQUE':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[58,-21,-22,-23,-24,-25,-26,-29,-30,-48,58,-37,58,-36,58,-46,58,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,58,58,-47,-27,-28,-49,-50,-51,58,58,58,58,-38,-39,]),'MENORQUE':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[59,-21,-22,-23,-24,-25,-26,-29,-30,-48,59,-37,59,-36,59,-46,59,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,59,59,-47,-27,-28,-49,-50,-51,59,59,59,59,-38,-39,]),'MAYORQUE':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[60,-21,-22,-23,-24,-25,-26,-29,-30,-48,60,-37,60,-36,60,-46,60,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,60,60,-47,-27,-28,-49,-50,-51,60,60,60,60,-38,-39,]),'MENORIQUE':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[61,-21,-22,-23,-24,-25,-26,-29,-30,-48,61,-37,61,-36,61,-46,61,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,61,61,-47,-27,-28,-49,-50,-51,61,61,61,61,-38,-39,]),'MAYORIQUE':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[62,-21,-22,-23,-24,-25,-26,-29,-30,-48,62,-37,62,-36,62,-46,62,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,62,62,-47,-27,-28,-49,-50,-51,62,62,62,62,-38,-39,]),'PTO':([24,25,26,27,28,29,30,31,32,36,46,48,49,64,68,72,75,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,115,116,120,121,122,123,],[63,-21,-22,-23,-24,-25,-26,-29,-30,-48,63,63,63,63,63,-46,63,63,63,63,63,63,63,63,63,63,63,63,63,63,-47,-27,-28,-49,-50,-51,63,63,63,63,-38,-39,]),'PTCOMA':([25,26,27,28,29,30,31,32,36,46,48,50,64,68,72,76,77,78,79,80,81,82,83,84,85,86,96,106,109,110,111,112,113,114,122,123,],[-21,-22,-23,-24,-25,-26,-29,-30,-48,70,-37,74,-36,95,-46,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,107,117,-47,-27,-28,-49,-50,-51,-38,-39,]),'AS':([25,26,27,28,29,30,31,32,36,48,49,64,72,76,77,78,79,80,81,82,83,84,85,86,109,110,111,112,113,114,122,123,],[-21,-22,-23,-24,-25,-26,-29,-30,-48,-37,73,-36,-46,-31,-32,-33,-34,-35,-40,-41,-42,-43,-44,-45,-47,-27,-28,-49,-50,-51,-38,-39,]),'DDOSPT':([34,35,],[65,66,]),'LLAVEIZQ':([47,],[71,]),'TOSTRING':([63,],[87,]),'TOOWNED':([63,],[88,]),'ABS':([63,],[89,]),'SQRT':([63,],[90,]),'CLONE':([63,],[91,]),'POW':([65,],[92,]),'POWF':([66,],[93,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'inicio':([0,],[1,]),'instrucciones':([0,8,71,],[2,14,97,]),'instruccion':([0,2,8,14,71,97,],[3,9,3,9,3,9,]),'imprimir':([0,2,8,14,71,97,],[4,4,4,4,4,4,]),'declaracion':([0,2,8,14,71,97,],[5,5,5,5,5,5,]),'main':([2,],[8,]),'expresiones':([16,],[23,]),'expresion':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[24,46,48,49,64,68,75,76,77,78,79,80,81,82,83,84,85,86,96,106,115,116,120,121,]),'tostring':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,]),'toowned':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,]),'nativas_fun':([16,19,21,22,33,38,51,52,53,54,55,56,57,58,59,60,61,62,69,94,104,105,118,119,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'tipo':([18,37,73,],[39,67,98,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> inicio","S'",1,None,None,None),
  ('inicio -> instrucciones main instrucciones','inicio',3,'p_inicio_inicio','Sintactico.py',83),
  ('main -> FN MAIN PARIZQ PARDER LLAVEIZQ instrucciones LLAVEDER','main',7,'p_main','Sintactico.py',115),
  ('instrucciones -> instrucciones instruccion','instrucciones',2,'p_instrucciones1','Sintactico.py',136),
  ('instrucciones -> instruccion','instrucciones',1,'p_instrucciones2','Sintactico.py',142),
  ('instrucciones -> <empty>','instrucciones',0,'p_instrucciones3','Sintactico.py',146),
  ('instruccion -> imprimir','instruccion',1,'p_instrucion','Sintactico.py',153),
  ('instruccion -> declaracion','instruccion',1,'p_instrucion','Sintactico.py',154),
  ('imprimir -> PRINTLN NOT PARIZQ expresiones PARDER PTCOMA','imprimir',6,'p_imprimir2','Sintactico.py',373),
  ('declaracion -> LET MUT ID DOSPT tipo IGUAL expresion PTCOMA','declaracion',8,'p_declaracion1','Sintactico.py',382),
  ('declaracion -> LET MUT ID IGUAL expresion PTCOMA','declaracion',6,'p_declaracion2','Sintactico.py',387),
  ('declaracion -> LET ID DOSPT tipo IGUAL expresion PTCOMA','declaracion',7,'p_declaracion3','Sintactico.py',392),
  ('declaracion -> LET ID IGUAL expresion PTCOMA','declaracion',5,'p_declaracion4','Sintactico.py',397),
  ('tipo -> I64','tipo',1,'p_tipo1','Sintactico.py',582),
  ('tipo -> F64','tipo',1,'p_tipo1','Sintactico.py',583),
  ('tipo -> BOOL','tipo',1,'p_tipo1','Sintactico.py',584),
  ('tipo -> CHAR','tipo',1,'p_tipo1','Sintactico.py',585),
  ('tipo -> STRING','tipo',1,'p_tipo1','Sintactico.py',586),
  ('tipo -> USIZE','tipo',1,'p_tipo1','Sintactico.py',587),
  ('expresiones -> expresiones COMA expresion','expresiones',3,'p_expresiones1','Sintactico.py',613),
  ('expresiones -> expresion','expresiones',1,'p_expresiones2','Sintactico.py',621),
  ('expresion -> ENTERO','expresion',1,'p_expresion_entero','Sintactico.py',633),
  ('expresion -> DECIMAL','expresion',1,'p_expresion_decimal','Sintactico.py',640),
  ('expresion -> TRUE','expresion',1,'p_expresion_true','Sintactico.py',647),
  ('expresion -> FALSE','expresion',1,'p_expresion_false','Sintactico.py',652),
  ('expresion -> tostring','expresion',1,'p_expresion_to','Sintactico.py',659),
  ('expresion -> toowned','expresion',1,'p_expresion_to','Sintactico.py',660),
  ('tostring -> expresion PTO TOSTRING PARIZQ PARDER','tostring',5,'p_expresion_tostring','Sintactico.py',667),
  ('toowned -> expresion PTO TOOWNED PARIZQ PARDER','toowned',5,'p_expresion_toowned','Sintactico.py',672),
  ('expresion -> CADENA','expresion',1,'p_expresion_cadena1','Sintactico.py',681),
  ('expresion -> CARACTER','expresion',1,'p_expresion_caracter','Sintactico.py',688),
  ('expresion -> expresion MAS expresion','expresion',3,'p_expresion_aritmetica1','Sintactico.py',695),
  ('expresion -> expresion MENOS expresion','expresion',3,'p_expresion_aritmetica1','Sintactico.py',696),
  ('expresion -> expresion POR expresion','expresion',3,'p_expresion_aritmetica1','Sintactico.py',697),
  ('expresion -> expresion DIVIDIDO expresion','expresion',3,'p_expresion_aritmetica1','Sintactico.py',698),
  ('expresion -> expresion MODULO expresion','expresion',3,'p_expresion_aritmetica1','Sintactico.py',699),
  ('expresion -> MENOS expresion','expresion',2,'p_exp_unaria','Sintactico.py',718),
  ('expresion -> NOT expresion','expresion',2,'p_exp_unaria','Sintactico.py',719),
  ('expresion -> I64 DDOSPT POW PARIZQ expresion COMA expresion PARDER','expresion',8,'p_expresion_aritmetica2','Sintactico.py',732),
  ('expresion -> F64 DDOSPT POWF PARIZQ expresion COMA expresion PARDER','expresion',8,'p_expresion_aritmetica2','Sintactico.py',733),
  ('expresion -> expresion IGUALQUE expresion','expresion',3,'p_expresion_relacional','Sintactico.py',747),
  ('expresion -> expresion NOIGUALQUE expresion','expresion',3,'p_expresion_relacional','Sintactico.py',748),
  ('expresion -> expresion MENORQUE expresion','expresion',3,'p_expresion_relacional','Sintactico.py',749),
  ('expresion -> expresion MAYORQUE expresion','expresion',3,'p_expresion_relacional','Sintactico.py',750),
  ('expresion -> expresion MENORIQUE expresion','expresion',3,'p_expresion_relacional','Sintactico.py',751),
  ('expresion -> expresion MAYORIQUE expresion','expresion',3,'p_expresion_relacional','Sintactico.py',752),
  ('expresion -> PARIZQ expresion PARDER','expresion',3,'p_exp_agrupa','Sintactico.py',770),
  ('expresion -> PARIZQ expresion AS tipo PARDER','expresion',5,'p_casteo','Sintactico.py',936),
  ('expresion -> nativas_fun','expresion',1,'p_funciones_nat_inicio','Sintactico.py',944),
  ('nativas_fun -> expresion PTO ABS PARIZQ PARDER','nativas_fun',5,'p_funciones_nat1','Sintactico.py',949),
  ('nativas_fun -> expresion PTO SQRT PARIZQ PARDER','nativas_fun',5,'p_funciones_nat1','Sintactico.py',950),
  ('nativas_fun -> expresion PTO CLONE PARIZQ PARDER','nativas_fun',5,'p_funciones_nat2','Sintactico.py',960),
]