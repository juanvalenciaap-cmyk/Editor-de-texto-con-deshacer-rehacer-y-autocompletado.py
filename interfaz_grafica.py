import tkinter as tk
from tkinter import ttk, font
# Usar esta cosa es como si usaramos un xaml(Amo C# 😍) 
# Solo que esto es python puro, todo se escribe en python (Por eso no me gusta ahhhhh)
class EditorVisualMockup(tk.Tk):
    """
    Apartado visual (mockup) del Editor de Texto.
    Desacoplado de la lógica de estructuras de datos por el momento. (Despues la ponemos para que quede melisimo)
    """
    def __init__(self):
        super().__init__()
        
        self.title("Editor de Texto Super Divertido Para Toda La Familia")
        self.geometry("950;650".replace(";", "x"))
        self.minsize(700, 450)

        # Paleta de colores estilo oscuro
        self.colores = {
            "bg_principal": "#1e1e2e",
            "bg_secundario": "#181825",
            "bg_editor": "#11111b",
            "bg_numeros": "#181825",
            "fg_texto": "#cdd6f4",
            "fg_numeros": "#585b70",
            "accent": "#89b4fa",
            "accent_hover": "#b4befe",
            "panel_border": "#313244",
            "sugerencia_bg": "#24273a",
            "sugerencia_sel": "#363a4f",
            "status_bg": "#181825",
            "status_fg": "#a6adc8"
        }

        self.configure(bg=self.colores["bg_principal"])

        # Tipografías
        self.fuente_editor = font.Font(family="Consolas", size=12)
        self.fuente_ui = font.Font(family="Segoe UI", size=10)
        self.fuente_ui_bold = font.Font(family="Segoe UI", size=10, weight="bold")

        self._crear_menu_superior()
        self._crear_barra_herramientas()
        self._crear_panel_busqueda()
        self._crear_cuerpo_editor()
        self._crear_popup_autocompletado()
        self._crear_barra_estado()

        # Cargar texto demo e inicializar vista
        self._cargar_demo()
        self._actualizar_numeros_linea()

    # ---------------------------------------------------------
    # 1. Menú superior de la ventana
    # ---------------------------------------------------------
    def _crear_menu_superior(self):
        self.barra_menus = tk.Menu(self)

        # Menú Archivo
        menu_archivo = tk.Menu(self.barra_menus, tearoff=0)
        menu_archivo.add_command(label="Nuevo", accelerator="Ctrl+N")
        menu_archivo.add_command(label="Abrir archivo...", accelerator="Ctrl+O")
        menu_archivo.add_command(label="Guardar", accelerator="Ctrl+S")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.quit)
        self.barra_menus.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú Estructuras
        menu_estructuras = tk.Menu(self.barra_menus, tearoff=0)
        menu_estructuras.add_command(label="Cargar Diccionario de Palabras...")
        menu_estructuras.add_command(label="Ver Historial de Operaciones")
        self.barra_menus.add_cascade(label="Estructuras", menu=menu_estructuras)

        self.config(menu=self.barra_menus)

    # ---------------------------------------------------------
    # 2. Barra de herramientas interna (Toolbar)
    # ---------------------------------------------------------
    def _crear_barra_herramientas(self):
        self.toolbar = tk.Frame(self, bg=self.colores["bg_secundario"], height=42, padx=8, pady=4)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        def crear_boton_tool(texto, comando=None):
            btn = tk.Button(
                self.toolbar,
                text=texto,
                bg=self.colores["bg_secundario"],
                fg=self.colores["fg_texto"],
                activebackground=self.colores["panel_border"],
                activeforeground=self.colores["accent"],
                relief=tk.FLAT,
                bd=0,
                padx=12,
                pady=4,
                font=self.fuente_ui,
                cursor="hand2",
                command=comando
            )
            btn.pack(side=tk.LEFT, padx=3)
            return btn

        # Operaciones de edición dentro del programa
        crear_boton_tool("⟲ Deshacer")
        crear_boton_tool("⟳ Rehacer")

        tk.Frame(self.toolbar, bg=self.colores["panel_border"], width=1, height=20).pack(side=tk.LEFT, padx=8, pady=4)

        crear_boton_tool("🔍 Buscar y Reemplazar", self._toggle_panel_busqueda)

        # Separador y botón de demo de sugerencias
        tk.Frame(self.toolbar, bg=self.colores["panel_border"], width=1, height=20).pack(side=tk.LEFT, padx=8, pady=4)
        crear_boton_tool("✨ Sugerencias (Demo)", self._simular_autocompletado)

    # ---------------------------------------------------------
    # 3. Panel de Búsqueda y Reemplazo (Ocultable)
    # ---------------------------------------------------------
    def _crear_panel_busqueda(self):
        self.panel_busqueda = tk.Frame(self, bg=self.colores["bg_secundario"], padx=10, pady=6, bd=1, relief=tk.SOLID)
        
        # Etiqueta y campo Buscar
        tk.Label(self.panel_busqueda, text="Buscar:", bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], font=self.fuente_ui).grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.entry_buscar = tk.Entry(self.panel_busqueda, width=22, bg=self.colores["bg_editor"], fg=self.colores["fg_texto"], insertbackground=self.colores["fg_texto"], relief=tk.FLAT, font=self.fuente_ui)
        self.entry_buscar.grid(row=0, column=1, padx=5, pady=2)

        # Botones de Búsqueda
        btn_buscar_siguiente = tk.Button(self.panel_busqueda, text="Buscar Siguiente", bg=self.colores["panel_border"], fg=self.colores["fg_texto"], relief=tk.FLAT, font=self.fuente_ui, cursor="hand2")
        btn_buscar_siguiente.grid(row=0, column=2, padx=4, pady=2)

        # Etiqueta y campo Reemplazar
        tk.Label(self.panel_busqueda, text="Reemplazar:", bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], font=self.fuente_ui).grid(row=0, column=3, padx=5, pady=2, sticky="e")
        self.entry_reemplazar = tk.Entry(self.panel_busqueda, width=22, bg=self.colores["bg_editor"], fg=self.colores["fg_texto"], insertbackground=self.colores["fg_texto"], relief=tk.FLAT, font=self.fuente_ui)
        self.entry_reemplazar.grid(row=0, column=4, padx=5, pady=2)

        # Botones de Reemplazo
        btn_reemplazar = tk.Button(self.panel_busqueda, text="Reemplazar", bg=self.colores["panel_border"], fg=self.colores["fg_texto"], relief=tk.FLAT, font=self.fuente_ui, cursor="hand2")
        btn_reemplazar.grid(row=0, column=5, padx=4, pady=2)

        btn_reemplazar_todo = tk.Button(self.panel_busqueda, text="Reemplazar Todo", bg=self.colores["panel_border"], fg=self.colores["fg_texto"], relief=tk.FLAT, font=self.fuente_ui, cursor="hand2")
        btn_reemplazar_todo.grid(row=0, column=6, padx=4, pady=2)

        # Botón Cerrar panel
        btn_cerrar = tk.Button(self.panel_busqueda, text="✕", bg=self.colores["bg_secundario"], fg=self.colores["fg_texto"], relief=tk.FLAT, font=self.fuente_ui_bold, cursor="hand2", command=self._toggle_panel_busqueda)
        btn_cerrar.grid(row=0, column=7, padx=8, pady=2)

        self.busqueda_visible = False

    def _toggle_panel_busqueda(self):
        if self.busqueda_visible:
            self.panel_busqueda.pack_forget()
            self.busqueda_visible = False
        else:
            self.panel_busqueda.pack(side=tk.TOP, fill=tk.X, after=self.toolbar)
            self.busqueda_visible = True
            self.entry_buscar.focus_set()

    # ---------------------------------------------------------
    # 4. Área de texto central y número de líneas
    # ---------------------------------------------------------
    def _crear_cuerpo_editor(self):
        contenedor_editor = tk.Frame(self, bg=self.colores["bg_principal"])
        contenedor_editor.pack(fill=tk.BOTH, expand=True)

        # Barra de scroll vertical
        self.scroll_y = tk.Scrollbar(contenedor_editor, bg=self.colores["bg_secundario"])
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Números de línea (Text widget deshabilitado para escribir)
        self.numeros_linea = tk.Text(
            contenedor_editor,
            width=4,
            padx=8,
            pady=8,
            takefocus=0,
            border=0,
            bg=self.colores["bg_numeros"],
            fg=self.colores["fg_numeros"],
            state=tk.DISABLED,
            font=self.fuente_editor,
            wrap=tk.NONE
        )
        self.numeros_linea.pack(side=tk.LEFT, fill=tk.Y)

        # Área de edición principal
        self.texto_editor = tk.Text(
            contenedor_editor,
            padx=12,
            pady=8,
            border=0,
            bg=self.colores["bg_editor"],
            fg=self.colores["fg_texto"],
            insertbackground=self.colores["accent"], # Color del cursor
            selectbackground=self.colores["panel_border"],
            selectforeground=self.colores["fg_texto"],
            font=self.fuente_editor,
            undo=False, # Manejado por nuestra propia lógica posteriormente
            wrap=tk.NONE,
            yscrollcommand=self._sincronizar_scroll
        )
        self.texto_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_y.config(command=self._on_scroll_scrollbar)

        # Eventos para sincronizar números de línea y conteos
        self.texto_editor.bind("<KeyRelease>", self._on_cambio_contenido)
        self.texto_editor.bind("<MouseWheel>", self._on_scroll_mouse)
        self.texto_editor.bind("<Button-1>", lambda e: self.popup_sugerencias.place_forget())

    def _sincronizar_scroll(self, primero, ultimo):
        self.scroll_y.set(primero, ultimo)
        self.numeros_linea.yview_moveto(primero)

    def _on_scroll_scrollbar(self, *args):
        self.texto_editor.yview(*args)
        self.numeros_linea.yview(*args)

    def _on_scroll_mouse(self, event):
        self._actualizar_numeros_linea()

    def _on_cambio_contenido(self, event=None):
        self._actualizar_numeros_linea()
        self._actualizar_info_estado()

    def _actualizar_numeros_linea(self):
        lineas_totales = int(self.texto_editor.index("end-1c").split(".")[0])
        lista_numeros = "\n".join(str(i) for i in range(1, lineas_totales + 1))

        self.numeros_linea.config(state=tk.NORMAL)
        self.numeros_linea.delete("1.0", tk.END)
        self.numeros_linea.insert("1.0", lista_numeros)
        self.numeros_linea.config(state=tk.DISABLED)

        # Sincronizar posición vertical
        primero, _ = self.texto_editor.yview()
        self.numeros_linea.yview_moveto(primero)

    # ---------------------------------------------------------
    # 5. Ventana emergente (Popup) de autocompletado
    # ---------------------------------------------------------
    def _crear_popup_autocompletado(self):
        self.popup_sugerencias = tk.Frame(
            self.texto_editor,
            bg=self.colores["sugerencia_bg"],
            bd=1,
            relief=tk.SOLID
        )

        tk.Label(
            self.popup_sugerencias,
            text=" Sugerencias (Tab / Enter)",
            bg=self.colores["panel_border"],
            fg=self.colores["accent"],
            font=font.Font(family="Segoe UI", size=8, weight="bold"),
            anchor="w"
        ).pack(fill=tk.X)

        self.lista_sugerencias = tk.Listbox(
            self.popup_sugerencias,
            height=5,
            width=24,
            bg=self.colores["sugerencia_bg"],
            fg=self.colores["fg_texto"],
            selectbackground=self.colores["accent"],
            selectforeground=self.colores["bg_secundario"],
            relief=tk.FLAT,
            bd=0,
            font=self.fuente_ui,
            activestyle="none"
        )
        self.lista_sugerencias.pack(padx=2, pady=2)

    def _simular_autocompletado(self):
        """Muestra cómo se ve el menú flotante de autocompletado."""
        self.lista_sugerencias.delete(0, tk.END)
        ejemplos = ["estructura", "estudiante", "estático", "estimación", "estrategia"]
        for p in ejemplos:
            self.lista_sugerencias.insert(tk.END, f"  {p}")

        self.lista_sugerencias.selection_set(0)

        # Ubicar cerca de donde esté el cursor (coordenadas aproximadas)
        bbox = self.texto_editor.bbox(tk.INSERT)
        if bbox:
            x, y, _, alto = bbox
            self.popup_sugerencias.place(x=x + 10, y=y + alto + 5)
        else:
            self.popup_sugerencias.place(x=120, y=60)

    # ---------------------------------------------------------
    # 6. Barra de estado inferior
    # ---------------------------------------------------------
    def _crear_barra_estado(self):
        self.barra_estado = tk.Frame(self, bg=self.colores["status_bg"], height=26, padx=12)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

        # Conteo de líneas y caracteres
        self.lbl_conteo = tk.Label(
            self.barra_estado,
            text="Líneas: 1  |  Caracteres: 0",
            bg=self.colores["status_bg"],
            fg=self.colores["status_fg"],
            font=self.fuente_ui
        )
        self.lbl_conteo.pack(side=tk.LEFT)

        # Indicador de estado del historial (deshacer / rehacer)
        self.lbl_historial = tk.Label(
            self.barra_estado,
            text="Historial: 0 acciones disponibles",
            bg=self.colores["status_bg"],
            fg=self.colores["status_fg"],
            font=self.fuente_ui
        )
        self.lbl_historial.pack(side=tk.RIGHT, padx=15)

        # Estado de codificación
        self.lbl_encoding = tk.Label(
            self.barra_estado,
            text="UTF-8",
            bg=self.colores["status_bg"],
            fg=self.colores["status_fg"],
            font=self.fuente_ui
        )
        self.lbl_encoding.pack(side=tk.RIGHT, padx=10)

    def _actualizar_info_estado(self):
        texto = self.texto_editor.get("1.0", "end-1c")
        num_caracteres = len(texto)
        num_lineas = int(self.texto_editor.index("end-1c").split(".")[0])
        self.lbl_conteo.config(text=f"Líneas: {num_lineas}  |  Caracteres: {num_caracteres}")

    # ---------------------------------------------------------
    # Texto de demostración inicial
    # ---------------------------------------------------------
    def _cargar_demo(self):
        demo = (
            "# ==========================================================\n"
            "# Editor de Texto con Deshacer, Rehacer y Autocompletado\n"
            "# ==========================================================\n\n"
            "Bienvenido al entorno visual del proyecto.\n"
            "Esta maqueta visual incluye:\n"
            " - Barra de herramientas con accesos rápidos (Nuevo, Abrir, Guardar, Deshacer, Rehacer).\n"
            " - Panel retráctil para 'Buscar y Reemplazar'.\n"
            " - Numeración lateral de líneas sincronizada.\n"
            " - Ventana emergente (popup) para sugerencias de autocompletado.\n"
            " - Barra de estado inferior (conteo de líneas/caracteres y estado de historial).\n"
            "Anda, prueba a escribir algo, vas a ver que divertido como funciona todo Jajjaja, no, no va a funcionar\n"
            "NO HAY LOGICA CONECTADA AÚN 😊"
        )
        self.texto_editor.insert("1.0", demo)
        self._actualizar_info_estado()


if __name__ == "__main__":
    app = EditorVisualMockup()
    app.mainloop()
