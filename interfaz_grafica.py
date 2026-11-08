
import os
import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox

from logica import Logica


class EditorTexto(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("Documento 1 — Editor de Texto")
        self.geometry("1100x720")
        self.minsize(800, 500)

        self.logica = Logica()

        # si existe un diccionario.txt junto al programa
        # se carga en lugar del por defecto (si falla se conserva
        # el diccionario por defecto y el arranque sigue normal)
        ruta_diccionario = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "diccionario.txt"
        )
        if os.path.exists(ruta_diccionario):
            try:
                self.logica.cargar_diccionario(ruta_diccionario)
            except Exception:
                pass

        # Paleta de colores
        self.colores = {
            "office_blue":       "#185abd",
            "office_blue_dark":  "#103f80",
            "office_blue_light": "#e8f0fe",
            "toolbar_bg":        "#ffffff",  
            "toolbar_border":    "#e2e4e9",
            "canvas_bg":         "#e9edf4",  
            "hoja_bg":           "#ffffff",  
            "hoja_borde":        "#cfd4dc",
            "texto_color":       "#1f2328",
            "texto_secundario":  "#5f6368",
            "numeros_bg":        "#f8f9fa",
            "numeros_fg":        "#80868b",
            "numeros_borde":     "#e0e0e0",
            "hover_btn":         "#f0f2f5",
            "active_btn":        "#dbeafe",  
            "status_bg":         "#185abd",  
            "status_fg":         "#ffffff",
            "busqueda_hl":       "#fff176", 
            "busqueda_fg":       "#000000",
            "sugerencia_bg":     "#ffffff",
            "sugerencia_sel":    "#185abd",
            "sugerencia_sel_fg": "#ffffff",
        }

        self.configure(bg=self.colores["toolbar_bg"])

        # Tipografías base
        self.fuente_ui_familia = "Segoe UI"
        self.fuente_base = font.Font(family="Calibri", size=11)
        self.fuente_numeros = font.Font(family="Consolas", size=10)

        # Estado de edición y formato
        self._es_negrita = False
        self._es_cursiva = False
        self._es_subrayado = False
        self._ultimo_snapshot = ""
        self._nombre_archivo_actual = "Documento 1"
        self._modificado = False
        self._ultima_busqueda = ""
        self._lineas_gutter = 0
        self._archivos_recientes = []

        # Construcción de la interfaz
        self._configurar_estilos_ttk()
        self._crear_barra_herramientas()
        self._crear_panel_busqueda()
        self._crear_area_editor()
        self._crear_popup_autocompletado()
        self._crear_barra_estado()

        # Atajos de teclado globales
        self.bind_all("<Control-z>", self._deshacer)
        self.bind_all("<Control-y>", self._rehacer)
        self.bind_all("<Control-n>", lambda e: self._nuevo_documento())
        self.bind_all("<Control-o>", lambda e: self._abrir_archivo())
        self.bind_all("<Control-s>", lambda e: self._guardar_archivo())
        self.bind_all("<Control-f>", lambda e: self._toggle_panel_busqueda())
        self.bind_all("<Control-b>", lambda e: self._toggle_negrita())
        self.bind_all("<Control-i>", lambda e: self._toggle_cursiva())
        self.bind_all("<Control-u>", lambda e: self._toggle_subrayado())

        # Inicialización de vista
        self._sincronizar_altura_gutter()
        self._actualizar_numeros_linea()
        self._actualizar_info_estado()

    # =========================================================================
    # 1. CONFIGURACIÓN VISUAL Y MENÚ ARCHIVO
    # =========================================================================

    def _configurar_estilos_ttk(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Toolbar.TCombobox",
            fieldbackground="#ffffff",
            background=self.colores["toolbar_bg"],
            foreground=self.colores["texto_color"],
            relief="flat",
            padding=3
        )

        # scrollbar delgada y plana, acorde al diseño de la interfaz
        style.configure(
            "Vertical.TScrollbar",
            background="#f1f3f4",
            troughcolor="#f8f9fa",
            bordercolor=self.colores["toolbar_border"],
            arrowcolor=self.colores["texto_secundario"],
            relief="flat",
            width=12
        )

    def _sincronizar_altura_gutter(self):
        # iguala la altura de cada linea de los numeros de linea con la del
        # editor: si difieren, el desfase se acumula con cada linea y los
        # numeros acaban desalineados del texto
        objetivo = self.fuente_base.metrics("linespace")
        elegido = None
        for tamano in range(8, 15):
            self.fuente_numeros.configure(size=tamano)
            if self.fuente_numeros.metrics("linespace") <= objetivo:
                elegido = tamano
            else:
                break
        if elegido is None:
            elegido = 8
        self.fuente_numeros.configure(size=elegido)
        # spacing1 cubre la diferencia exacta: la altura de linea del gutter
        # mas spacing1 queda igual a la altura de linea del editor
        restante = objetivo - self.fuente_numeros.metrics("linespace")
        self.numeros_linea.configure(spacing1=max(0, restante))

    def _desplegar_menu_archivo(self):
        # Despliega el menú del botón Archivo 
        menu = tk.Menu(
            self,
            tearoff=0,
            font=(self.fuente_ui_familia, 9),
            bg="#ffffff",
            fg=self.colores["texto_color"],
            activebackground=self.colores["office_blue"],
            activeforeground="#ffffff",
            bd=1,
            relief=tk.SOLID
        )

        menu.add_command(label="📄  Nuevo documento", accelerator="Ctrl+N", command=self._nuevo_documento)
        menu.add_command(label="📂  Abrir archivo...", accelerator="Ctrl+O", command=self._abrir_archivo)
        menu.add_command(label="💾  Guardar", accelerator="Ctrl+S", command=self._guardar_archivo)
        menu.add_command(label="💾  Guardar como...", command=self._guardar_como)
        menu.add_separator()

        # Diccionario de palabras sugeridas (solo carga desde archivo externo;
        # la edicion del diccionario se hace editando el .txt y recargandolo)
        menu.add_command(label="📖  Cargar diccionario...", command=self._cargar_diccionario)
        menu.add_command(label="↺  Diccionario por defecto", command=self._diccionario_por_defecto)
        menu.add_separator()

        # Submenú dinámico de archivos recientes
        menu_recientes = tk.Menu(
            menu,
            tearoff=0,
            font=(self.fuente_ui_familia, 9),
            bg="#ffffff",
            fg=self.colores["texto_color"],
            activebackground=self.colores["office_blue"],
            activeforeground="#ffffff"
        )

        if self._archivos_recientes:
            for ruta in self._archivos_recientes:
                nombre = os.path.basename(ruta)
                menu_recientes.add_command(
                    label=f"📄 {nombre}   ({ruta})",
                    command=lambda r=ruta: self._cargar_archivo_por_ruta(r)
                )
        else:
            menu_recientes.add_command(label="(No hay archivos recientes)", state="disabled")

        menu.add_cascade(label="🕒  Archivos recientes", menu=menu_recientes)
        menu.add_separator()
        menu.add_command(label="✕  Salir", command=self.quit)

        try:
            x = self.btn_archivo.winfo_rootx()
            y = self.btn_archivo.winfo_rooty() + self.btn_archivo.winfo_height() + 2
            menu.post(x, y)
        except Exception:
            pass

    def _agregar_archivo_reciente(self, ruta):
        # Registra una ruta en la lista de archivos recientes.
        if not ruta:
            return
        ruta_abs = os.path.abspath(ruta)
        if ruta_abs in self._archivos_recientes:
            self._archivos_recientes.remove(ruta_abs)
        self._archivos_recientes.insert(0, ruta_abs)
        if len(self._archivos_recientes) > 10:
            self._archivos_recientes.pop()

    # =========================================================================
    # 2. BARRA DE HERRAMIENTAS UNIFICADA
    # =========================================================================

    def _crear_barra_herramientas(self):
        self.toolbar_frame = tk.Frame(
            self,
            bg=self.colores["toolbar_bg"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colores["toolbar_border"]
        )
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        fila = tk.Frame(self.toolbar_frame, bg=self.colores["toolbar_bg"], padx=10, pady=6)
        fila.pack(side=tk.LEFT, fill=tk.X)

        # Botón destacado Archivo
        self.btn_archivo = tk.Button(
            fila,
            text="Archivo ▾",
            command=self._desplegar_menu_archivo,
            bg=self.colores["office_blue"],
            fg="#ffffff",
            activebackground=self.colores["office_blue_dark"],
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=4,
            font=(self.fuente_ui_familia, 9, "bold"),
            cursor="hand2"
        )
        self.btn_archivo.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_archivo.bind("<Enter>", lambda e: self.btn_archivo.config(bg=self.colores["office_blue_dark"]))
        self.btn_archivo.bind("<Leave>", lambda e: self.btn_archivo.config(bg=self.colores["office_blue"]))

        def btn_tool(padre, texto, comando, icono=""):
            txt = f"{icono} {texto}".strip() if icono else texto
            btn = tk.Button(
                padre,
                text=txt,
                command=comando,
                bg=self.colores["toolbar_bg"],
                fg=self.colores["texto_color"],
                activebackground=self.colores["active_btn"],
                activeforeground=self.colores["office_blue_dark"],
                relief=tk.FLAT,
                bd=0,
                padx=8,
                pady=4,
                font=(self.fuente_ui_familia, 9),
                cursor="hand2"
            )
            btn.bind("<Enter>", lambda e: btn.config(bg=self.colores["hover_btn"]))
            btn.bind("<Leave>", lambda e: btn.config(bg=self.colores["toolbar_bg"]))
            btn.pack(side=tk.LEFT, padx=1)
            return btn

        def separador():
            sep = tk.Frame(fila, width=1, height=22, bg=self.colores["toolbar_border"])
            sep.pack(side=tk.LEFT, padx=7, pady=2)

        separador()

        # Historial (Undo / Redo)
        self.btn_deshacer = btn_tool(fila, "Deshacer", self._deshacer, icono="⟲")
        self.btn_rehacer = btn_tool(fila, "Rehacer", self._rehacer, icono="⟳")

        separador()

        # Fuente y Tamaño
        self.cb_fuentes = ttk.Combobox(
            fila,
            values=["Calibri", "Arial", "Times New Roman", "Segoe UI", "Georgia", "Consolas"],
            width=14,
            state="readonly",
            style="Toolbar.TCombobox"
        )
        self.cb_fuentes.set("Calibri")
        self.cb_fuentes.bind("<<ComboboxSelected>>", self._cambiar_fuente)
        self.cb_fuentes.pack(side=tk.LEFT, padx=(2, 3))

        self.cb_tamano = ttk.Combobox(
            fila,
            values=[9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 36],
            width=3,
            state="readonly",
            style="Toolbar.TCombobox"
        )
        self.cb_tamano.set(11)
        self.cb_tamano.bind("<<ComboboxSelected>>", self._cambiar_tamano)
        self.cb_tamano.pack(side=tk.LEFT, padx=(0, 4))

        # Botones de estilo tipográfico N, K, S
        def btn_estilo(txt, cmd, fnt):
            b = tk.Button(
                fila,
                text=txt,
                command=cmd,
                font=fnt,
                width=3,
                relief=tk.FLAT,
                bd=0,
                padx=2,
                pady=3,
                bg=self.colores["toolbar_bg"],
                fg=self.colores["texto_color"],
                activebackground=self.colores["active_btn"],
                cursor="hand2"
            )
            b.pack(side=tk.LEFT, padx=1)
            return b

        self.btn_negrita = btn_estilo("N", self._toggle_negrita, (self.fuente_ui_familia, 9, "bold"))
        self.btn_cursiva = btn_estilo("K", self._toggle_cursiva, (self.fuente_ui_familia, 9, "italic"))
        self.btn_subrayado = btn_estilo("S", self._toggle_subrayado, (self.fuente_ui_familia, 9, "underline"))

        # Mayúsculas / Minúsculas rápidas
        btn_tool(fila, "Aa ↑", self._convertir_mayusculas)
        btn_tool(fila, "aa ↓", self._convertir_minusculas)

        separador()

        # Búsqueda y Reemplazo (un solo panel con los dos campos)
        btn_tool(fila, "Buscar y reemplazar", self._toggle_panel_busqueda, icono="🔍")

    # =========================================================================
    # 3. PANEL DE BÚSQUEDA Y REEMPLAZO FLOTANTE
    # =========================================================================

    def _crear_panel_busqueda(self):
        self.panel_busqueda = tk.Frame(
            self,
            bg="#ffffff",
            bd=1,
            relief=tk.SOLID,
            padx=12,
            pady=8
        )
        self.panel_busqueda.configure(highlightbackground=self.colores["toolbar_border"], highlightthickness=1)

        # Fila Búsqueda
        f1 = tk.Frame(self.panel_busqueda, bg="#ffffff")
        f1.pack(fill=tk.X, pady=2)

        tk.Label(f1, text="Buscar:", bg="#ffffff", fg=self.colores["texto_color"],
                 font=(self.fuente_ui_familia, 9), width=10, anchor="w").pack(side=tk.LEFT)

        self.entry_buscar = tk.Entry(
            f1, width=20, font=(self.fuente_ui_familia, 9),
            bg="#ffffff", fg=self.colores["texto_color"], bd=1, relief=tk.SOLID
        )
        self.entry_buscar.pack(side=tk.LEFT, padx=4)
        self.entry_buscar.bind("<Return>", lambda e: self._buscar_siguiente())

        tk.Button(
            f1, text="↓ Siguiente", command=self._buscar_siguiente,
            bg=self.colores["office_blue_light"], fg=self.colores["office_blue"],
            relief=tk.FLAT, bd=0, padx=8, pady=2, font=(self.fuente_ui_familia, 9, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            f1, text="✕", command=self._toggle_panel_busqueda,
            bg="#ffffff", fg=self.colores["texto_secundario"],
            relief=tk.FLAT, bd=0, padx=6, font=(self.fuente_ui_familia, 9, "bold"),
            cursor="hand2"
        ).pack(side=tk.RIGHT)

        # Fila Reemplazo
        f2 = tk.Frame(self.panel_busqueda, bg="#ffffff")
        f2.pack(fill=tk.X, pady=2)

        tk.Label(f2, text="Reemplazar:", bg="#ffffff", fg=self.colores["texto_color"],
                 font=(self.fuente_ui_familia, 9), width=10, anchor="w").pack(side=tk.LEFT)

        self.entry_reemplazar = tk.Entry(
            f2, width=20, font=(self.fuente_ui_familia, 9),
            bg="#ffffff", fg=self.colores["texto_color"], bd=1, relief=tk.SOLID
        )
        self.entry_reemplazar.pack(side=tk.LEFT, padx=4)
        self.entry_reemplazar.bind("<Return>", lambda e: self._reemplazar_actual())

        tk.Button(
            f2, text="Reemplazar", command=self._reemplazar_actual,
            bg=self.colores["hover_btn"], fg=self.colores["texto_color"],
            relief=tk.FLAT, bd=0, padx=6, pady=2, font=(self.fuente_ui_familia, 9),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            f2, text="Todo", command=self._reemplazar_todo,
            bg=self.colores["hover_btn"], fg=self.colores["texto_color"],
            relief=tk.FLAT, bd=0, padx=6, pady=2, font=(self.fuente_ui_familia, 9),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

        self.busqueda_visible = False

    def _toggle_panel_busqueda(self, event=None):
        if self.busqueda_visible:
            self.panel_busqueda.place_forget()
            self.busqueda_visible = False
            self.texto_editor.tag_remove("busqueda", "1.0", tk.END)
        else:
            # se coloca justo debajo de la toolbar (altura real, no fija)
            alto_toolbar = self.toolbar_frame.winfo_height()
            if alto_toolbar <= 1:      # la ventana aun no se ha pintado
                alto_toolbar = 95
            self.panel_busqueda.place(relx=1.0, y=alto_toolbar + 6, anchor="ne", x=-25)
            self.panel_busqueda.lift()
            self.busqueda_visible = True
            self.entry_buscar.focus_set()
            self.entry_buscar.select_range(0, tk.END)

    # =========================================================================
    # 4. ÁREA DE TRABAJO DEL EDITOR
    # =========================================================================

    def _crear_area_editor(self):
        self.contenedor_fondo = tk.Frame(self, bg=self.colores["canvas_bg"])
        self.contenedor_fondo.pack(fill=tk.BOTH, expand=True)

        self.scroll_y = ttk.Scrollbar(self.contenedor_fondo, style="Vertical.TScrollbar")
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        frame_centrado = tk.Frame(self.contenedor_fondo, bg=self.colores["canvas_bg"])
        frame_centrado.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)

        self.marco_hoja = tk.Frame(frame_centrado, bg=self.colores["hoja_borde"], bd=1, relief=tk.SOLID)
        self.marco_hoja.pack(fill=tk.BOTH, expand=True)

        self.hoja_interior = tk.Frame(self.marco_hoja, bg=self.colores["hoja_bg"])
        self.hoja_interior.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Números de línea laterales
        self.numeros_linea = tk.Text(
            self.hoja_interior,
            width=4,
            padx=8,
            pady=20,
            takefocus=0,
            border=0,
            bg=self.colores["numeros_bg"],
            fg=self.colores["numeros_fg"],
            state=tk.DISABLED,
            font=self.fuente_numeros,
            wrap=tk.NONE
        )
        self.numeros_linea.pack(side=tk.LEFT, fill=tk.Y)

        tk.Frame(self.hoja_interior, width=1, bg=self.colores["numeros_borde"]).pack(side=tk.LEFT, fill=tk.Y)

        # Widget de texto central
        self.texto_editor = tk.Text(
            self.hoja_interior,
            padx=35,
            pady=20,
            border=0,
            bg=self.colores["hoja_bg"],
            fg=self.colores["texto_color"],
            insertbackground=self.colores["office_blue"],
            selectbackground=self.colores["office_blue"],
            selectforeground="#ffffff",
            font=self.fuente_base,
            undo=False,
            wrap=tk.WORD,
            yscrollcommand=self._sincronizar_scroll
        )
        self.texto_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._configurar_tags_editor()
        self.scroll_y.config(command=self._on_scroll_scrollbar)

        # Enlace de eventos del editor
        self.texto_editor.bind("<KeyPress>", self._on_key_press)
        self.texto_editor.bind("<KeyRelease>", self._on_tecla_liberada)
        self.texto_editor.bind("<MouseWheel>", self._on_scroll_mouse)
        self.texto_editor.bind("<Button-1>", self._on_click_editor)
        self.texto_editor.bind("<Tab>", self._aplicar_sugerencia)
        self.texto_editor.bind("<Return>", self._on_enter)
        self.texto_editor.bind("<Left>", lambda e: self._mover_cursor_logica("izquierda"))
        self.texto_editor.bind("<Right>", lambda e: self._mover_cursor_logica("derecha"))
        self.texto_editor.bind("<Up>", lambda e: self._mover_cursor_logica("arriba"))
        self.texto_editor.bind("<Down>", lambda e: self._mover_cursor_logica("abajo"))

    def _configurar_tags_editor(self):
        familia = self.fuente_base.actual("family")
        tamano = self.fuente_base.actual("size")

        self.texto_editor.tag_config(
            "busqueda",
            background=self.colores["busqueda_hl"],
            foreground=self.colores["busqueda_fg"]
        )
        self.texto_editor.tag_config("negrita", font=(familia, tamano, "bold"))
        self.texto_editor.tag_config("cursiva", font=(familia, tamano, "italic"))
        self.texto_editor.tag_config("negrita_cursiva", font=(familia, tamano, "bold italic"))
        self.texto_editor.tag_config("subrayado", underline=True)

    def _sincronizar_scroll(self, primero, ultimo):
        self.scroll_y.set(primero, ultimo)
        self.numeros_linea.yview_moveto(primero)

    def _on_scroll_scrollbar(self, *args):
        self.texto_editor.yview(*args)
        self.numeros_linea.yview(*args)

    def _on_scroll_mouse(self, event):
        self._actualizar_numeros_linea()

    def _mover_cursor_logica(self, direccion, event=None):
        # el movimiento de las flechas lo decide la Logica: primero se
        # sincroniza su cursor con la posicion real del widget, se le pide el
        # movimiento y luego el widget lo respeta
        pos = self.texto_editor.index(tk.INSERT).split(".")
        self.logica.set_cursor(int(pos[0]) - 1, int(pos[1]))
        self.logica.mover_cursor(direccion)
        destino = f"{self.logica.cursor._fila + 1}.{self.logica.cursor._columna}"
        self.texto_editor.mark_set(tk.INSERT, destino)
        self.texto_editor.see(destino)
        self._actualizar_info_estado()
        return "break"

    def _on_click_editor(self, event=None):
        self.popup_sugerencias.place_forget()
        self._sincronizar_botones_con_cursor()
        self._actualizar_info_estado()

    def _sincronizar_botones_con_cursor(self):
        """Refleja en los botones N, K, S el formato presente en la posición del cursor."""
        try:
            pos = self.texto_editor.index(tk.INSERT)
            check_pos = f"{pos}-1c" if pos.split(".")[1] != "0" else pos
            tags = self.texto_editor.tag_names(check_pos)
            self._es_negrita = "negrita" in tags or "negrita_cursiva" in tags
            self._es_cursiva = "cursiva" in tags or "negrita_cursiva" in tags
            self._es_subrayado = "subrayado" in tags

            self._actualizar_boton_estilo(self.btn_negrita, self._es_negrita)
            self._actualizar_boton_estilo(self.btn_cursiva, self._es_cursiva)
            self._actualizar_boton_estilo(self.btn_subrayado, self._es_subrayado)
        except Exception:
            pass

    def _actualizar_numeros_linea(self):
        lineas_totales = int(self.texto_editor.index("end-1c").split(".")[0])

        # solo se regenera el gutter si cambio la cantidad de lineas;
        # en las demas teclas es suficiente sincronizar el scroll
        if lineas_totales != self._lineas_gutter:
            self._lineas_gutter = lineas_totales
            lista_numeros = "\n".join(str(i) for i in range(1, lineas_totales + 1))

            self.numeros_linea.config(state=tk.NORMAL)
            self.numeros_linea.delete("1.0", tk.END)
            self.numeros_linea.insert("1.0", lista_numeros)
            self.numeros_linea.config(state=tk.DISABLED)

        primero, _ = self.texto_editor.yview()
        self.numeros_linea.yview_moveto(primero)

    # =========================================================================
    # 5. AUTOCOMPLETADO FLOTANTE (BST + DICCIONARIO)
    # =========================================================================

    def _crear_popup_autocompletado(self):
        self.popup_sugerencias = tk.Frame(self.texto_editor, bg=self.colores["sugerencia_bg"], bd=1, relief=tk.SOLID)
        self.popup_sugerencias.configure(highlightbackground=self.colores["office_blue"], highlightthickness=1)

        tk.Label(
            self.popup_sugerencias,
            text="  Sugerencias de palabra (Tab)",
            bg=self.colores["office_blue_light"],
            fg=self.colores["office_blue"],
            font=(self.fuente_ui_familia, 8, "bold"),
            anchor="w"
        ).pack(fill=tk.X)

        self.lista_sugerencias = tk.Listbox(
            self.popup_sugerencias,
            height=5,
            width=24,
            bg=self.colores["sugerencia_bg"],
            fg=self.colores["texto_color"],
            selectbackground=self.colores["sugerencia_sel"],
            selectforeground=self.colores["sugerencia_sel_fg"],
            relief=tk.FLAT,
            bd=0,
            font=(self.fuente_ui_familia, 9),
            activestyle="none"
        )
        self.lista_sugerencias.pack(padx=2, pady=2)
        self.lista_sugerencias.bind("<Return>", self._aplicar_sugerencia)
        self.lista_sugerencias.bind("<Tab>", self._aplicar_sugerencia)

    def _actualizar_autocompletado(self):
        pos = self.texto_editor.index(tk.INSERT)
        num_linea = pos.split(".")[0]
        texto_hasta_cursor = self.texto_editor.get(f"{num_linea}.0", pos)

        tokens = texto_hasta_cursor.split()
        if not tokens:
            self.popup_sugerencias.place_forget()
            return

        prefijo = tokens[-1]
        if len(prefijo) < 2:
            self.popup_sugerencias.place_forget()
            return

        sugerencias = self.logica.sugerir_palabras(prefijo)
        if not sugerencias:
            self.popup_sugerencias.place_forget()
            return

        self.lista_sugerencias.delete(0, tk.END)
        for s in sugerencias:
            self.lista_sugerencias.insert(tk.END, f"  {s}")
        self.lista_sugerencias.selection_set(0)

        bbox = self.texto_editor.bbox(tk.INSERT)
        if bbox:
            x, y, _, alto = bbox
            self.popup_sugerencias.place(x=x + 10, y=y + alto + 4)
        else:
            self.popup_sugerencias.place(x=40, y=40)

    def _aplicar_sugerencia(self, event=None):
        if not self.popup_sugerencias.winfo_ismapped():
            return

        seleccion = self.lista_sugerencias.curselection()
        if not seleccion:
            return "break"

        palabra_completa = self.lista_sugerencias.get(seleccion[0]).strip()
        pos = self.texto_editor.index(tk.INSERT)
        num_linea = pos.split(".")[0]
        texto_hasta_cursor = self.texto_editor.get(f"{num_linea}.0", pos)

        tokens = texto_hasta_cursor.split()
        if tokens:
            prefijo = tokens[-1]
            col_inicio = len(texto_hasta_cursor) - len(prefijo)
            inicio_tk = f"{num_linea}.{col_inicio}"
            texto_previo = self.texto_editor.get("1.0", "end-1c")
            self.texto_editor.delete(inicio_tk, pos)
            self.texto_editor.insert(inicio_tk, palabra_completa + " ")

            texto_nuevo = self.texto_editor.get("1.0", "end-1c")
            self.logica.cargar_texto(texto_nuevo)
            self.logica.guardar_snapshot(texto_previo)
            self._ultimo_snapshot = texto_nuevo
            self._marcar_modificado(True)

        self.popup_sugerencias.place_forget()
        self._actualizar_numeros_linea()
        self._actualizar_info_estado()
        return "break"

    # =========================================================================
    # 6. GESTIÓN DE EDICIÓN Y ESTILOS DE FORMATO
    # =========================================================================

    def _on_tecla_liberada(self, event=None):
        texto_actual = self.texto_editor.get("1.0", "end-1c")
        self.logica.cargar_texto(texto_actual)

        # Se apila siempre el estado ANTERIOR de la ultima edicion registrada.
        # Asi cada operacion (escritura, borrado, pegado) es un paso de deshacer
        # y el documento original siempre queda guardado en pila_undo.
        if texto_actual != self._ultimo_snapshot:
            self.logica.guardar_snapshot(self._ultimo_snapshot)
            self._ultimo_snapshot = texto_actual
            self._marcar_modificado(True)

        self._actualizar_autocompletado()
        self._actualizar_numeros_linea()
        self._actualizar_info_estado(texto_actual)

    def _on_enter(self, event=None):
        texto_actual = self.texto_editor.get("1.0", "end-1c")
        if texto_actual != self._ultimo_snapshot:
            self.logica.guardar_snapshot(self._ultimo_snapshot)
            self._ultimo_snapshot = texto_actual
        self.popup_sugerencias.place_forget()
        return None

    def _cambiar_fuente(self, event=None):
        familia = self.cb_fuentes.get()
        tamano = int(self.cb_tamano.get())
        self.fuente_base.configure(family=familia, size=tamano)
        self._configurar_tags_editor()
        # al cambiar la fuente del texto hay que realinear los numeros de linea
        self._sincronizar_altura_gutter()

    def _cambiar_tamano(self, event=None):
        self._cambiar_fuente()

    def _obtener_tags_activos(self):
        """Retorna la lista de tags que deben aplicarse a los caracteres escritos."""
        tags = []
        if self._es_negrita and self._es_cursiva:
            tags.append("negrita_cursiva")
        elif self._es_negrita:
            tags.append("negrita")
        elif self._es_cursiva:
            tags.append("cursiva")

        if self._es_subrayado:
            tags.append("subrayado")
        return tags

    def _on_key_press(self, event):
        """Aplica estilos activos únicamente al texto que se teclea sin alterar lo previo."""
        if event.char and event.char >= " " and not (event.state & 0x4):
            tags_activos = self._obtener_tags_activos()

            try:
                sel_inicio = self.texto_editor.index(tk.SEL_FIRST)
                sel_fin = self.texto_editor.index(tk.SEL_LAST)
                self.texto_editor.delete(sel_inicio, sel_fin)
            except tk.TclError:
                pass

            pos_antes = self.texto_editor.index(tk.INSERT)
            self.texto_editor.insert(tk.INSERT, event.char, tuple(tags_activos))
            pos_despues = self.texto_editor.index(tk.INSERT)

            # Limpiar herencias indeseadas si algún estilo está desactivado
            if not self._es_negrita:
                self.texto_editor.tag_remove("negrita", pos_antes, pos_despues)
                self.texto_editor.tag_remove("negrita_cursiva", pos_antes, pos_despues)
            if not self._es_cursiva:
                self.texto_editor.tag_remove("cursiva", pos_antes, pos_despues)
                self.texto_editor.tag_remove("negrita_cursiva", pos_antes, pos_despues)
            if not self._es_subrayado:
                self.texto_editor.tag_remove("subrayado", pos_antes, pos_despues)

            self._on_tecla_liberada(event)
            return "break"
        return None

    def _actualizar_boton_estilo(self, btn, activo):
        if activo:
           
            btn.config(
                bg=self.colores["office_blue"],
                fg="#ffffff",
                relief=tk.FLAT,
                bd=0,
                highlightthickness=0
            )
        else:
            btn.config(
                bg=self.colores["toolbar_bg"],
                fg=self.colores["texto_color"],
                relief=tk.FLAT,
                bd=0,
                highlightthickness=0
            )

    def _toggle_negrita(self):
        try:
            inicio = self.texto_editor.index(tk.SEL_FIRST)
            fin = self.texto_editor.index(tk.SEL_LAST)
            hay_seleccion = True
        except tk.TclError:
            hay_seleccion = False

        if hay_seleccion:
            tags = self.texto_editor.tag_names(inicio)
            tiene_neg = "negrita" in tags or "negrita_cursiva" in tags
            tiene_cur = "cursiva" in tags or "negrita_cursiva" in tags

            if tiene_neg:
                self.texto_editor.tag_remove("negrita", inicio, fin)
                self.texto_editor.tag_remove("negrita_cursiva", inicio, fin)
                if tiene_cur:
                    self.texto_editor.tag_add("cursiva", inicio, fin)
                self._es_negrita = False
            else:
                if tiene_cur:
                    self.texto_editor.tag_remove("cursiva", inicio, fin)
                    self.texto_editor.tag_add("negrita_cursiva", inicio, fin)
                else:
                    self.texto_editor.tag_add("negrita", inicio, fin)
                self._es_negrita = True
        else:
            self._es_negrita = not self._es_negrita

        self._actualizar_boton_estilo(self.btn_negrita, self._es_negrita)
        self.texto_editor.focus_set()

    def _toggle_cursiva(self):
        try:
            inicio = self.texto_editor.index(tk.SEL_FIRST)
            fin = self.texto_editor.index(tk.SEL_LAST)
            hay_seleccion = True
        except tk.TclError:
            hay_seleccion = False

        if hay_seleccion:
            tags = self.texto_editor.tag_names(inicio)
            tiene_neg = "negrita" in tags or "negrita_cursiva" in tags
            tiene_cur = "cursiva" in tags or "negrita_cursiva" in tags

            if tiene_cur:
                self.texto_editor.tag_remove("cursiva", inicio, fin)
                self.texto_editor.tag_remove("negrita_cursiva", inicio, fin)
                if tiene_neg:
                    self.texto_editor.tag_add("negrita", inicio, fin)
                self._es_cursiva = False
            else:
                if tiene_neg:
                    self.texto_editor.tag_remove("negrita", inicio, fin)
                    self.texto_editor.tag_add("negrita_cursiva", inicio, fin)
                else:
                    self.texto_editor.tag_add("cursiva", inicio, fin)
                self._es_cursiva = True
        else:
            self._es_cursiva = not self._es_cursiva

        self._actualizar_boton_estilo(self.btn_cursiva, self._es_cursiva)
        self.texto_editor.focus_set()

    def _toggle_subrayado(self):
        try:
            inicio = self.texto_editor.index(tk.SEL_FIRST)
            fin = self.texto_editor.index(tk.SEL_LAST)
            hay_seleccion = True
        except tk.TclError:
            hay_seleccion = False

        if hay_seleccion:
            if "subrayado" in self.texto_editor.tag_names(inicio):
                self.texto_editor.tag_remove("subrayado", inicio, fin)
                self._es_subrayado = False
            else:
                self.texto_editor.tag_add("subrayado", inicio, fin)
                self._es_subrayado = True
        else:
            self._es_subrayado = not self._es_subrayado

        self._actualizar_boton_estilo(self.btn_subrayado, self._es_subrayado)
        self.texto_editor.focus_set()

    def _convertir_mayusculas(self):
        try:
            inicio = self.texto_editor.index(tk.SEL_FIRST)
            fin = self.texto_editor.index(tk.SEL_LAST)
            texto_sel = self.texto_editor.get(inicio, fin)
            self.texto_editor.delete(inicio, fin)
            self.texto_editor.insert(inicio, texto_sel.upper())
            self._on_tecla_liberada()
        except tk.TclError:
            pass

    def _convertir_minusculas(self):
        try:
            inicio = self.texto_editor.index(tk.SEL_FIRST)
            fin = self.texto_editor.index(tk.SEL_LAST)
            texto_sel = self.texto_editor.get(inicio, fin)
            self.texto_editor.delete(inicio, fin)
            self.texto_editor.insert(inicio, texto_sel.lower())
            self._on_tecla_liberada()
        except tk.TclError:
            pass

    # =========================================================================
    # 7. HISTORIAL (DESHACER Y REHACER)
    # =========================================================================

    def _deshacer(self, event=None):
        texto_actual = self.texto_editor.get("1.0", "end-1c")
        self.logica.cargar_texto(texto_actual)

        texto_restaurado = self.logica.deshacer()
        if texto_restaurado is None:
            return "break"

        self._sincronizar_editor_desde_logica(texto_restaurado)
        return "break"

    def _rehacer(self, event=None):
        texto_restaurado = self.logica.rehacer()
        if texto_restaurado is None:
            return "break"

        self._sincronizar_editor_desde_logica(texto_restaurado)
        return "break"

    def _sincronizar_editor_desde_logica(self, texto):
        self.texto_editor.delete("1.0", tk.END)
        self.texto_editor.insert("1.0", texto)
        self._ultimo_snapshot = texto
        self.popup_sugerencias.place_forget()
        self._actualizar_numeros_linea()
        self._actualizar_info_estado()

    # =========================================================================
    # 8. BÚSQUEDA Y REEMPLAZO CON COLA DINÁMICA
    # =========================================================================

    def _buscar_siguiente(self):
        termino = self.entry_buscar.get()
        if not termino:
            return

        if termino != self._ultima_busqueda:
            self._ultima_busqueda = termino
            texto_actual = self.texto_editor.get("1.0", "end-1c")
            self.logica.cargar_texto(texto_actual)
            self.logica._reconstruir_arbol()
            coincidencias = self.logica.buscar_texto(termino)

            if not coincidencias:
                messagebox.showinfo("Búsqueda", f'No se encontró "{termino}".')
                self.texto_editor.tag_remove("busqueda", "1.0", tk.END)
                return

        resultado = self.logica.siguiente_coincidencia()
        if resultado is None:
            return

        fila, col = resultado
        longitud = len(termino)
        inicio = f"{fila + 1}.{col}"
        fin = f"{fila + 1}.{col + longitud}"

        self.texto_editor.tag_remove("busqueda", "1.0", tk.END)
        self.texto_editor.tag_add("busqueda", inicio, fin)
        self.texto_editor.see(inicio)
        self.texto_editor.mark_set(tk.INSERT, inicio)

    def _reemplazar_actual(self):
        termino = self.entry_buscar.get()
        reemplazo = self.entry_reemplazar.get()
        if not termino:
            return

        rangos = self.texto_editor.tag_ranges("busqueda")
        if not rangos:
            self._buscar_siguiente()
            return

        inicio, fin = rangos[0], rangos[1]
        texto_previo = self.texto_editor.get("1.0", "end-1c")
        self.texto_editor.delete(inicio, fin)
        self.texto_editor.insert(inicio, reemplazo)

        texto_nuevo = self.texto_editor.get("1.0", "end-1c")
        self.logica.cargar_texto(texto_nuevo)
        self.logica.guardar_snapshot(texto_previo)
        self._ultimo_snapshot = texto_nuevo
        self._marcar_modificado(True)

        self._ultima_busqueda = ""
        self._buscar_siguiente()

    def _reemplazar_todo(self):
        buscar = self.entry_buscar.get()
        reemplazar = self.entry_reemplazar.get()
        if not buscar:
            return

        texto_actual = self.texto_editor.get("1.0", "end-1c")
        self.logica.cargar_texto(texto_actual)
        self.logica.guardar_snapshot()

        conteo = self.logica.reemplazar_todo(buscar, reemplazar)
        if conteo > 0:
            self._sincronizar_editor_desde_logica(self.logica.obtener_texto())
            self._marcar_modificado(True)
            messagebox.showinfo("Reemplazar Todo", f"Se reemplazaron {conteo} apariciones.")
        else:
            messagebox.showinfo("Reemplazar Todo", f'No se encontró "{buscar}".')

        self._ultima_busqueda = ""
        self.texto_editor.tag_remove("busqueda", "1.0", tk.END)

    # =========================================================================
    # 9. GESTIÓN DE ARCHIVOS
    # =========================================================================

    def _nuevo_documento(self):
        if not self._confirmar_descarte():
            return
        self.logica.nuevo_documento()
        self.texto_editor.delete("1.0", tk.END)
        self._ultimo_snapshot = ""
        self._ultima_busqueda = ""
        self._nombre_archivo_actual = "Documento 1"
        self._marcar_modificado(False)
        self.texto_editor.tag_remove("busqueda", "1.0", tk.END)
        self._actualizar_numeros_linea()
        self._actualizar_info_estado()

    def _cargar_archivo_por_ruta(self, ruta):
        if not self._confirmar_descarte():
            return
        try:
            nodo = self.logica.abrir_archivo(ruta)
            texto = self.logica.obtener_texto()
            self.texto_editor.delete("1.0", tk.END)
            self.texto_editor.insert("1.0", texto)
            self._ultimo_snapshot = texto
            self._ultima_busqueda = ""
            self._nombre_archivo_actual = nodo.nombre
            self._marcar_modificado(False)
            self._agregar_archivo_reciente(ruta)
            self.texto_editor.tag_remove("busqueda", "1.0", tk.END)
            self._actualizar_numeros_linea()
            self._actualizar_info_estado()
        except Exception as e:
            messagebox.showerror("Error al abrir", str(e))

    def _abrir_archivo(self):
        if not self._confirmar_descarte():
            return
        ruta = filedialog.askopenfilename(
            title="Abrir documento",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return
        self._cargar_archivo_por_ruta(ruta)

    def _guardar_archivo(self):
        if self.logica.ruta_actual:
            texto_actual = self.texto_editor.get("1.0", "end-1c")
            self.logica.cargar_texto(texto_actual)
            try:
                self.logica.guardar_archivo()
                self._marcar_modificado(False)
                self._agregar_archivo_reciente(self.logica.ruta_actual)
            except Exception as e:
                messagebox.showerror("Error al guardar", str(e))
        else:
            self._guardar_como()

    def _guardar_como(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar documento",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return
        texto_actual = self.texto_editor.get("1.0", "end-1c")
        self.logica.cargar_texto(texto_actual)
        try:
            self.logica.guardar_archivo(ruta)
            self._nombre_archivo_actual = os.path.basename(ruta)
            self._marcar_modificado(False)
            self._agregar_archivo_reciente(ruta)
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def _cargar_diccionario(self):
        ruta = filedialog.askopenfilename(
            title="Cargar diccionario de palabras sugeridas",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return
        try:
            cantidad = self.logica.cargar_diccionario(ruta)
        except Exception as e:
            messagebox.showerror("Error al cargar diccionario", str(e))
            return
        if cantidad == 0:
            messagebox.showwarning(
                "Diccionario",
                "El archivo no contiene palabras válidas.\nSe mantiene el diccionario actual."
            )
        else:
            messagebox.showinfo("Diccionario", f"Diccionario cargado: {cantidad} palabras")

    def _diccionario_por_defecto(self):
        cantidad = self.logica.restaurar_diccionario_por_defecto()
        messagebox.showinfo(
            "Diccionario", f"Diccionario por defecto restaurado: {cantidad} palabras"
        )

    def _confirmar_descarte(self):
        if self._modificado:
            resp = messagebox.askyesnocancel(
                "¿Guardar cambios?",
                f"¿Deseas guardar los cambios en {self._nombre_archivo_actual} antes de continuar?"
            )
            if resp is True:
                self._guardar_archivo()
                return True
            elif resp is False:
                return True
            else:
                return False
        return True

    def _marcar_modificado(self, estado):
        self._modificado = estado
        asterisco = "• " if estado else ""
        self.title(f"{asterisco}{self._nombre_archivo_actual} — Editor de Texto")

    # =========================================================================
    # 10. BARRA DE ESTADO INFERIOR
    # =========================================================================

    def _crear_barra_estado(self):
        self.barra_estado = tk.Frame(self, bg=self.colores["status_bg"], height=26, padx=14)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_stats = tk.Label(
            self.barra_estado,
            text="0 palabras  |  0 caracteres  |  1 líneas",
            bg=self.colores["status_bg"],
            fg=self.colores["status_fg"],
            font=(self.fuente_ui_familia, 9)
        )
        self.lbl_stats.pack(side=tk.LEFT)

        lbl_zoom = tk.Label(
            self.barra_estado,
            text="100%",
            bg=self.colores["status_bg"],
            fg=self.colores["status_fg"],
            font=(self.fuente_ui_familia, 9)
        )
        lbl_zoom.pack(side=tk.RIGHT, padx=(10, 0))

        self.lbl_cursor = tk.Label(
            self.barra_estado,
            text="Lín 1, Col 1",
            bg=self.colores["status_bg"],
            fg=self.colores["status_fg"],
            font=(self.fuente_ui_familia, 9)
        )
        self.lbl_cursor.pack(side=tk.RIGHT, padx=10)

        self.lbl_historial = tk.Label(
            self.barra_estado,
            text="Historial: 0",
            bg=self.colores["status_bg"],
            fg=self.colores["status_fg"],
            font=(self.fuente_ui_familia, 9)
        )
        self.lbl_historial.pack(side=tk.RIGHT, padx=10)

        self.lbl_bitacora = tk.Label(
            self.barra_estado,
            text="Historial de acciones: 0",
            bg=self.colores["status_bg"],
            fg=self.colores["status_fg"],
            font=(self.fuente_ui_familia, 9)
        )
        self.lbl_bitacora.pack(side=tk.RIGHT, padx=10)

    def _actualizar_info_estado(self, texto=None):
        if texto is None:
            texto = self.texto_editor.get("1.0", "end-1c")
        num_chars = len(texto)
        palabras = len(texto.split()) if texto.strip() else 0
        num_lineas = texto.count("\n") + 1

        pos = self.texto_editor.index(tk.INSERT).split(".")
        self.logica.set_cursor(int(pos[0]) - 1, int(pos[1]))
        lin_act = self.logica.cursor._fila + 1
        col_act = self.logica.cursor._columna + 1

        self.lbl_stats.config(
            text=f"{palabras} palabras  |  {num_chars} caracteres  |  {num_lineas} líneas"
        )
        self.lbl_cursor.config(text=f"Lín {lin_act}, Col {col_act}")

        deshacer_n = self.logica.pila_undo.tamano()
        rehacer_n = self.logica.pila_redo.tamano()
        self.lbl_historial.config(text=f"⟲ {deshacer_n} | ⟳ {rehacer_n}")

        # historial de acciones registradas (una por paso de deshacer)
        total = self.logica.total_acciones()
        ultima = self.logica.ultima_operacion()
        self.lbl_bitacora.config(
            text=f"Historial de acciones: {total}" + (f" · últ: {ultima}" if ultima else "")
        )


if __name__ == "__main__":
    app = EditorTexto()
    app.mainloop()
