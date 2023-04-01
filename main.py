from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import uic
from datetime import datetime, timedelta
import json
import qdarktheme
 
class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'C:\Users\anton\Documents\GitHub\gp-counter\gui.ui', self)

        self.data = {}

        self.logs = []

        self.current_date = datetime.today()
        self.lbl_current_date.setText(self.current_date.strftime('%d/%m/%Y'))

        # Botones mover fecha
        self.btn_back_date.clicked.connect(self.back_date)
        self.btn_forward_date.clicked.connect(self.forward_date)

        # Botones gepear
        self.btn_gp_sergio.clicked.connect(lambda: self.change_gp("Sergio"))
        self.btn_gp_paula.clicked.connect(lambda: self.change_gp("Paula"))
        self.btn_gp_aina.clicked.connect(lambda: self.change_gp("Aina"))
        self.btn_gp_anton.clicked.connect(lambda: self.change_gp("Anton"))
        self.btn_gp_aitor.clicked.connect(lambda: self.change_gp("Aitor"))
        self.btn_gp_diego.clicked.connect(lambda: self.change_gp("Diego"))
        self.btn_gp_joaquin.clicked.connect(lambda: self.change_gp("Joaquin"))
        self.btn_gp_laura.clicked.connect(lambda: self.change_gp("Laura"))
        self.btn_gp_miranda.clicked.connect(lambda: self.change_gp("Miranda"))
        self.btn_gp_nerea.clicked.connect(lambda: self.change_gp("Nerea"))

        # Botones profeta
        self.btn_drg.clicked.connect(self.toggle_drg)
        self.btn_retraso.clicked.connect(self.toggle_retraso)
        self.btn_fallo.clicked.connect(self.toggle_fallo)

        # Botones faltas
        self.btn_amarilla.clicked.connect(self.amarilla)


        # Acciones
        self.actionAbrir.triggered.connect(self.load_file)
        self.actionGuardar.triggered.connect(self.save_file)
        self.actionGenerar_reporte.triggered.connect(self.report)

        self.actionLimpiar_dia.triggered.connect(self.limpiar_dia)

        # Otros
        self.btn_limpiar.clicked.connect(self.clean_log_window)

        self.log("Bienvenido a gp-counter\nADVERTENCIA: Al generar el reporte se muestra el rango de fechas pero puede estar equivocado. Ni puto caso.")

    def load_file(self):
        with open("datos.gp", "r") as loadfile:
            self.data = json.load(loadfile)

        self.log("Archivo cargado")
        self.update()

    def save_file(self):
        with open("datos.gp", "w") as savefile:
            json.dump(self.data, savefile)

        self.log("Archivo guardado en /datos.gp")

    def back_date(self):
        self.current_date -= timedelta(days=1)
        self.update()

    def forward_date(self):
        self.current_date += timedelta(days=1)
        self.update()

    def limpiar_dia(self):
        if self.check_day_entry_exists(self.current_date.strftime('%d/%m/%Y')):
            self.data.pop(self.current_date.strftime('%d/%m/%Y'))
        self.update()

        self.log("Día eliminado")
            

    def change_gp(self, player):
        current_date = self.current_date.strftime('%d/%m/%Y')

        # comprobar si el gp ya existe
        if current_date in self.data:
            if player in self.data[current_date]["GP"]:
                #el jugador ya ha gepeado; eliminar gepeo
                self.data[current_date]["GP"].remove(player)
            else:
                self.data[current_date]["GP"].append(player)

        # crear fecha nueva y ejecutar esto de nuevo
        else:
            self.create_new_date(current_date)
            self.change_gp(player)

        self.update()

    def create_new_date(self, date):
        if date in self.data:
            pass
        else:
            self.data[date] = {
                "GP": [], # se guardan en orden
                "FALTAS": [],
                "PROFETA": []
            }

    def toggle_drg(self):
        current_date = self.current_date.strftime('%d/%m/%Y')
        if current_date in self.data:
            if "Drg" in self.data[current_date]["PROFETA"]:
                self.data[current_date]["PROFETA"].remove("Drg")
            else:
                self.data[current_date]["PROFETA"].append("Drg")
        else:
            self.create_new_date(current_date)
            self.toggle_drg()

        self.update()
    
    def toggle_retraso(self):
        current_date = self.current_date.strftime('%d/%m/%Y')
        if current_date in self.data:
            if "retraso" in self.data[current_date]["PROFETA"]:
                self.data[current_date]["PROFETA"].remove("retraso")
            else:
                self.data[current_date]["PROFETA"].append("retraso")
        else:
            self.create_new_date(current_date)
            self.toggle_retraso()

        self.update()
    
    def toggle_fallo(self):
        current_date = self.current_date.strftime('%d/%m/%Y')
        if current_date in self.data:
            if "fallo" in self.data[current_date]["PROFETA"]:
                self.data[current_date]["PROFETA"].remove("fallo")
            else:
                self.data[current_date]["PROFETA"].append("fallo")
        else:
            self.create_new_date(current_date)
            self.toggle_fallo()

        self.update()

    def amarilla(self):
        uic.loadUi("amarilla.ui", self)

    def log(self, text):
        self.logs.append(text + "\n")
        self.update()
        print(text)
        self.logWindow.setText("".join(self.logs))

        with open("log.txt", "a") as log:
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log.write("[" + dt_string + "]" + " " + text + "\n")

    def clean_log_window(self):
        self.logWindow.setText("")
        self.logs = []
        
    # cada vez que se cambia de fecha básicamente
    def update(self):
        current_date = self.current_date.strftime('%d/%m/%Y')
        self.lbl_current_date.setText(current_date)
        
        #actualizar label con info
        label_text = self.get_info_label(current_date)
        self.lbl_display_info.setText(label_text)

        # actualizar botones. esto se podria hacer loopeando por los nombres de funciones pero no sé como se hace eso
        if self.check_day_entry_exists(current_date):
            if "Sergio" in self.data[current_date]["GP"]:
                self.btn_gp_sergio.setStyleSheet("background-color : green")
            else:
                self.btn_gp_sergio.setStyleSheet("")
            if "Paula" in self.data[current_date]["GP"]:
                self.btn_gp_paula.setStyleSheet("background-color : green")
            else:
                self.btn_gp_paula.setStyleSheet("")
            if "Aina" in self.data[current_date]["GP"]:
                self.btn_gp_aina.setStyleSheet("background-color : green")
            else:
                self.btn_gp_aina.setStyleSheet("")
            if "Anton" in self.data[current_date]["GP"]:
                self.btn_gp_anton.setStyleSheet("background-color : green")
            else:
                self.btn_gp_anton.setStyleSheet("")
            if "Aitor" in self.data[current_date]["GP"]:
                self.btn_gp_aitor.setStyleSheet("background-color : green")
            else:
                self.btn_gp_aitor.setStyleSheet("")
            if "Diego" in self.data[current_date]["GP"]:
                self.btn_gp_diego.setStyleSheet("background-color : green")
            else:
                self.btn_gp_diego.setStyleSheet("")
            if "Joaquin" in self.data[current_date]["GP"]:
                self.btn_gp_joaquin.setStyleSheet("background-color : green")
            else:
                self.btn_gp_joaquin.setStyleSheet("")
            if "Laura" in self.data[current_date]["GP"]:
                self.btn_gp_laura.setStyleSheet("background-color : green")
            else:
                self.btn_gp_laura.setStyleSheet("")
            if "Miranda" in self.data[current_date]["GP"]:
                self.btn_gp_miranda.setStyleSheet("background-color : green")
            else:
                self.btn_gp_miranda.setStyleSheet("")
            if "Nerea" in self.data[current_date]["GP"]:
                self.btn_gp_nerea.setStyleSheet("background-color : green")
            else:
                self.btn_gp_nerea.setStyleSheet("")

            # PROFETA
            if "Drg" in self.data[current_date]["PROFETA"]:
                self.btn_drg.setStyleSheet("background-color : blue")
            else:
                self.btn_drg.setStyleSheet("")
            if "retraso" in self.data[current_date]["PROFETA"]:
                self.btn_retraso.setStyleSheet("background-color : blue")
            else:
                self.btn_retraso.setStyleSheet("")
            if "fallo" in self.data[current_date]["PROFETA"]:
                self.btn_fallo.setStyleSheet("background-color : blue")
            else:
                self.btn_fallo.setStyleSheet("")
            
        else:
            self.btn_gp_sergio.setStyleSheet("")
            self.btn_gp_paula.setStyleSheet("")
            self.btn_gp_aina.setStyleSheet("")
            self.btn_gp_anton.setStyleSheet("")
            self.btn_gp_aitor.setStyleSheet("")
            self.btn_gp_diego.setStyleSheet("")
            self.btn_gp_joaquin.setStyleSheet("")
            self.btn_gp_laura.setStyleSheet("")
            self.btn_gp_miranda.setStyleSheet("")
            self.btn_gp_nerea.setStyleSheet("")

            self.btn_drg.setStyleSheet("")
            self.btn_retraso.setStyleSheet("")
            self.btn_fallo.setStyleSheet("")

            

    def check_day_entry_exists(self, date):
        if date in self.data:
            return True
        else:
            return False

    # devuelve texto con el resumen del día
    def get_info_label(self, date):
        try:
            day_data = self.data[date]
            label = "GPs: " + ", ".join(day_data["GP"]) + "\n" + "FALTAS: " + ", ".join(day_data["FALTAS"]) + "\n" + "PROFETA: " + ", ".join(day_data["PROFETA"])
            return label
        except KeyError:
            return "Sin datos para esta fecha"
        
    def report(self):
        gp_list = []
        profeta_list = []
        first_gps_list = []

        first_day = list(self.data.keys())[0]
        last_day = list(self.data.keys())[-1]
        
        for day in self.data:
            first_gepeador = self.data[day]['GP'][0]
            first_gps_list.append(first_gepeador)

            gp_list = gp_list + self.data[day]['GP']

            profeta_list = profeta_list + self.data[day]['PROFETA']

        # CUENTAS GP

        dict_gps = {
            "Sergio": gp_list.count('Sergio'),
            "Paula": gp_list.count('Paula'),
            "Aina": gp_list.count('Aina'),
            "Anton": gp_list.count('Anton'),
            "Aitor": gp_list.count('Aitor'),
            "Diego": gp_list.count('Diego'),
            "Joaquin": gp_list.count('Joaquin'),
            "Laura": gp_list.count('Laura'),
            "Miranda": gp_list.count('Miranda'),
            "Nerea": gp_list.count('Nerea'),
        }
        dict_gps = dict(sorted(dict_gps.items(), key=lambda item: item[1], reverse=True))

        dict_first_gps = {
            "Sergio": first_gps_list.count('Sergio'),
            "Paula": first_gps_list.count('Paula'),
            "Aina": first_gps_list.count('Aina'),
            "Anton": first_gps_list.count('Anton'),
            "Aitor": first_gps_list.count('Aitor'),
            "Diego": first_gps_list.count('Diego'),
            "Joaquin": first_gps_list.count('Joaquin'),
            "Laura": first_gps_list.count('Laura'),
            "Miranda": first_gps_list.count('Miranda'),
            "Nerea": first_gps_list.count('Nerea'),
        }
        dict_first_gps = dict(sorted(dict_first_gps.items(), key=lambda item: item[1], reverse=True))

        dict_profeta = {
            "Drg": profeta_list.count("Drg"),
            "Retrasos": profeta_list.count("retraso"),
            "Fallos": profeta_list.count("fallo")
        }

        gps_str = "--- GPs ---\n"
        for key, value in dict_gps.items():
            gps_str += f'{key}: {value}\n'

        first_gps_str = "--- PRIMEROS GPs ---\n"
        for key, value in dict_first_gps.items():
            first_gps_str += f'{key}: {value}\n'

        profeta_str = "--- PROFETA ---\n"
        for key, value in dict_profeta.items():
            profeta_str += f'{key}: {value}\n'



        # printear reporte
        final_report = "REPORTE: " + first_day + " - " + last_day + "\n" + gps_str + "\n" + first_gps_str + "\n" + profeta_str
        self.log(final_report)

        with open("reporte.txt", "w") as reporte:
            reporte.write(final_report)


app = QApplication([])
app.setStyle("Fusion")
qdarktheme.setup_theme()
window = UI()
window.show()
app.exec()