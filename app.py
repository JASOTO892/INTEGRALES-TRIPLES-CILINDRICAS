import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
from sympy import symbols, integrate, lambdify, sin, cos, sqrt, pi, exp, log
import warnings
warnings.filterwarnings('ignore')

def evaluar_funcion(funcion_str, r, theta, z):
    """
    Evalúa una función simbólica en coordenadas cilíndricas
    """
    try:
        # Definir símbolos
        r_sym, theta_sym, z_sym = symbols('r theta z')
        
        # Parsear la función
        funcion = sp.sympify(funcion_str)
        
        # Convertir a función numérica
        f_numeric = lambdify((r_sym, theta_sym, z_sym), funcion, 'numpy')
        
        return f_numeric(r, theta, z)
    except Exception as e:
        st.error(f"Error al evaluar la función: {e}")
        return None

def calcular_integral_triple(funcion_str, r_min, r_max, theta_min, theta_max, z_min, z_max):
    """
    Calcula la integral triple en coordenadas cilíndricas
    """
    try:
        # Definir símbolos
        r, theta, z = symbols('r theta z')
        
        # Parsear la función
        funcion = sp.sympify(funcion_str)
        
        # El jacobiano en coordenadas cilíndricas es r
        integrando = funcion * r
        
        # Calcular la integral triple
        st.info("Calculando integral... esto puede tomar un momento.")
        
        # Integrar respecto a z
        integral_z = integrate(integrando, (z, z_min, z_max))
        
        # Integrar respecto a theta
        integral_theta = integrate(integral_z, (theta, theta_min, theta_max))
        
        # Integrar respecto a r
        resultado = integrate(integral_theta, (r, r_min, r_max))
        
        return resultado, integrando
    except Exception as e:
        st.error(f"Error al calcular la integral: {e}")
        return None, None

def crear_grafico_region(r_min, r_max, theta_min, theta_max, z_min, z_max):
    """
    Crea un gráfico 3D de la región de integración
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Crear malla para la región cilíndrica
    theta_vals = np.linspace(theta_min, theta_max, 50)
    r_vals = np.linspace(r_min, r_max, 30)
    z_vals = np.linspace(z_min, z_max, 30)
    
    # Dibujar las superficies cilíndricas
    THETA, Z = np.meshgrid(theta_vals, z_vals)
    
    # Superficie cilíndrica interior
    if r_min > 0:
        X_inner = r_min * np.cos(THETA)
        Y_inner = r_min * np.sin(THETA)
        ax.plot_surface(X_inner, Y_inner, Z, alpha=0.3, color='blue', label='r mín')
    
    # Superficie cilíndrica exterior
    X_outer = r_max * np.cos(THETA)
    Y_outer = r_max * np.sin(THETA)
    ax.plot_surface(X_outer, Y_outer, Z, alpha=0.3, color='red', label='r máx')
    
    # Superficies planas (límites en theta)
    R, Z = np.meshgrid(r_vals, z_vals)
    
    # Plano theta = theta_min
    X_theta_min = R * np.cos(theta_min)
    Y_theta_min = R * np.sin(theta_min)
    ax.plot_surface(X_theta_min, Y_theta_min, Z, alpha=0.3, color='green')
    
    # Plano theta = theta_max
    X_theta_max = R * np.cos(theta_max)
    Y_theta_max = R * np.sin(theta_max)
    ax.plot_surface(X_theta_max, Y_theta_max, Z, alpha=0.3, color='green')
    
    # Superficies horizontales (límites en z)
    R, THETA = np.meshgrid(r_vals, theta_vals)
    X = R * np.cos(THETA)
    Y = R * np.sin(THETA)
    
    # Plano z = z_min
    Z_min = np.full_like(X, z_min)
    ax.plot_surface(X, Y, Z_min, alpha=0.3, color='yellow')
    
    # Plano z = z_max
    Z_max = np.full_like(X, z_max)
    ax.plot_surface(X, Y, Z_max, alpha=0.3, color='yellow')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Región de Integración en Coordenadas Cilíndricas')
    
    return fig

def crear_grafico_funcion(funcion_str, r_min, r_max, theta_min, theta_max, z_fijo):
    """
    Crea un gráfico 3D de la función en coordenadas cilíndricas
    """
    try:
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Crear malla
        r_vals = np.linspace(r_min, r_max, 30)
        theta_vals = np.linspace(theta_min, theta_max, 30)
        R, THETA = np.meshgrid(r_vals, theta_vals)
        
        # Convertir a coordenadas cartesianas
        X = R * np.cos(THETA)
        Y = R * np.sin(THETA)
        
        # Evaluar la función
        Z_vals = np.full_like(R, z_fijo)
        F = evaluar_funcion(funcion_str, R, THETA, Z_vals)
        
        if F is not None:
            # Crear gráfico de superficie
            surf = ax.plot_surface(X, Y, F, cmap='viridis', alpha=0.8)
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('f(r,θ,z)')
            ax.set_title(f'Función f(r,θ,z) = {funcion_str} en z = {z_fijo}')
        
        return fig
    except Exception as e:
        st.error(f"Error al crear el gráfico de la función: {e}")
        return None

# Configuración de la página
st.set_page_config(page_title="Integrales Triples Cilíndricas", page_icon="🔄", layout="wide")

# Título principal
st.title("🔄 Calculadora de Integrales Triples en Coordenadas Cilíndricas")
st.markdown("---")

# Descripción
st.markdown("""
Esta aplicación calcula integrales triples en coordenadas cilíndricas y muestra la visualización 3D.

**Fórmula de la integral triple cilíndrica:**
∭ f(r,θ,z) r dr dθ dz

**Coordenadas cilíndricas:**
- x = r cos(θ)
- y = r sin(θ)  
- z = z
- Jacobiano = r
""")

# Entrada de datos
st.subheader("📝 Configuración de la Integral")

# Función a integrar
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Función f(r,θ,z):**")
    funcion_str = st.text_input(
        "Ingresa la función (usa r, theta, z como variables):",
        value="r*z",
        help="Ejemplos: r*z, r**2*sin(theta), r*cos(theta)*z, r*exp(-z)"
    )
    
    st.markdown("**Funciones disponibles:**")
    st.markdown("- Trigonométricas: sin, cos, tan")
    st.markdown("- Exponencial: exp")
    st.markdown("- Logaritmo: log")
    st.markdown("- Raíz: sqrt")
    st.markdown("- Potencias: **")
    st.markdown("- Constantes: pi, e")

with col2:
    st.markdown("**Límites de integración:**")
    
    # Límites para r
    st.markdown("*Límites para r:*")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        r_min = st.number_input("r mín:", value=0.0, step=0.1)
    with col_r2:
        r_max = st.number_input("r máx:", value=2.0, step=0.1)
    
    # Límites para theta
    st.markdown("*Límites para θ:*")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        theta_min = st.number_input("θ mín:", value=0.0, step=0.1)
    with col_t2:
        theta_max = st.number_input("θ máx:", value=2*np.pi, step=0.1)
    
    # Límites para z
    st.markdown("*Límites para z:*")
    col_z1, col_z2 = st.columns(2)
    with col_z1:
        z_min = st.number_input("z mín:", value=0.0, step=0.1)
    with col_z2:
        z_max = st.number_input("z máx:", value=1.0, step=0.1)

# Botón para calcular
if st.button("🔄 Calcular Integral", type="primary"):
    if r_max > r_min and theta_max > theta_min and z_max > z_min:
        
        # Calcular la integral
        resultado, integrando = calcular_integral_triple(
            funcion_str, r_min, r_max, theta_min, theta_max, z_min, z_max
        )
        
        if resultado is not None:
            st.markdown("---")
            st.subheader("📊 Resultados")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("**Integral calculada:**")
                st.latex(f"\\int_{{{r_min}}}^{{{r_max}}} \\int_{{{theta_min}}}^{{{theta_max}}} \\int_{{{z_min}}}^{{{z_max}}} ({funcion_str}) \\cdot r \\, dz \\, d\\theta \\, dr")
                
                st.markdown("**Resultado:**")
                try:
                    resultado_numerico = float(resultado.evalf())
                    st.success(f"**{resultado_numerico:.6f}**")
                except:
                    st.success(f"**{resultado}**")
                
                st.markdown("**Integrando (con Jacobiano):**")
                st.write(f"({funcion_str}) × r = {integrando}")
            
            with col4:
                st.markdown("**Región de integración:**")
                st.write(f"• {r_min} ≤ r ≤ {r_max}")
                st.write(f"• {theta_min:.2f} ≤ θ ≤ {theta_max:.2f}")
                st.write(f"• {z_min} ≤ z ≤ {z_max}")
                
                # Convertir theta a grados para mejor comprensión
                theta_min_deg = theta_min * 180 / np.pi
                theta_max_deg = theta_max * 180 / np.pi
                st.write(f"• {theta_min_deg:.1f}° ≤ θ ≤ {theta_max_deg:.1f}°")
                
                # Volumen de la región
                volumen_region = (r_max**2 - r_min**2) * (theta_max - theta_min) * (z_max - z_min) / 2
                st.write(f"• Volumen de la región: {volumen_region:.4f}")
    else:
        st.error("❌ Los límites de integración no son válidos. Verifica que máx > mín.")

# Visualizaciones
st.markdown("---")
st.subheader("📈 Visualizaciones")

tab1, tab2 = st.tabs(["🏗️ Región de Integración", "📊 Gráfico de la Función"])

with tab1:
    st.markdown("**Región de integración en 3D:**")
    if st.button("🏗️ Mostrar Región"):
        try:
            fig_region = crear_grafico_region(r_min, r_max, theta_min, theta_max, z_min, z_max)
            st.pyplot(fig_region)
        except Exception as e:
            st.error(f"Error al crear el gráfico de la región: {e}")

with tab2:
    st.markdown("**Gráfico de la función f(r,θ,z):**")
    z_fijo = st.slider("Valor fijo de z para la visualización:", 
                       min_value=float(z_min), max_value=float(z_max), 
                       value=float((z_min + z_max) / 2), step=0.1)
    
    if st.button("📊 Mostrar Función"):
        try:
            fig_funcion = crear_grafico_funcion(funcion_str, r_min, r_max, theta_min, theta_max, z_fijo)
            if fig_funcion:
                st.pyplot(fig_funcion)
        except Exception as e:
            st.error(f"Error al crear el gráfico de la función: {e}")

# Ejemplos predefinidos
st.markdown("---")
st.subheader("💡 Ejemplos Predefinidos")

ejemplos = {
    "Cilindro simple": {
        "funcion": "1",
        "r_min": 0, "r_max": 2,
        "theta_min": 0, "theta_max": 2*np.pi,
        "z_min": 0, "z_max": 3
    },
    "Función lineal en z": {
        "funcion": "r*z",
        "r_min": 0, "r_max": 1,
        "theta_min": 0, "theta_max": np.pi,
        "z_min": 0, "z_max": 2
    },
    "Función trigonométrica": {
        "funcion": "r*cos(theta)",
        "r_min": 1, "r_max": 2,
        "theta_min": 0, "theta_max": np.pi/2,
        "z_min": 0, "z_max": 1
    },
    "Función exponencial": {
        "funcion": "r*exp(-z)",
        "r_min": 0, "r_max": 1,
        "theta_min": 0, "theta_max": 2*np.pi,
        "z_min": 0, "z_max": 1
    }
}

ejemplo_seleccionado = st.selectbox("Selecciona un ejemplo:", list(ejemplos.keys()))

if st.button("📋 Cargar Ejemplo"):
    ejemplo = ejemplos[ejemplo_seleccionado]
    st.session_state.update(ejemplo)
    st.rerun()

# Información adicional
st.markdown("---")
with st.expander("ℹ️ Información sobre Coordenadas Cilíndricas"):
    st.markdown("""
    **Coordenadas Cilíndricas (r, θ, z):**
    
    Las coordenadas cilíndricas son una extensión de las coordenadas polares al espacio tridimensional.
    
    **Transformación:**
    - x = r cos(θ)
    - y = r sin(θ)
    - z = z
    
    **Jacobiano:**
    El jacobiano de la transformación es **r**, por lo que:
    ```
    dx dy dz = r dr dθ dz
    ```
    
    **Integral Triple:**
    ```
    ∭ f(x,y,z) dx dy dz = ∭ f(r cos θ, r sin θ, z) r dr dθ dz
    ```
    
    **Aplicaciones:**
    - Cálculo de volúmenes con simetría cilíndrica
    - Centros de masa
    - Momentos de inercia
    - Problemas de física con simetría axial
    
    **Regiones típicas:**
    - Cilindros: 0 ≤ r ≤ R, 0 ≤ θ ≤ 2π
    - Sectores: 0 ≤ r ≤ R, α ≤ θ ≤ β
    - Anillos: r₁ ≤ r ≤ r₂, 0 ≤ θ ≤ 2π
    """)

with st.expander("🔧 Sintaxis para Funciones"):
    st.markdown("""
    **Sintaxis soportada:**
    
    **Variables:**
    - `r`: coordenada radial
    - `theta`: ángulo polar
    - `z`: coordenada vertical
    
    **Operaciones:**
    - `+`, `-`, `*`, `/`: operaciones básicas
    - `**`: potencia (ej: `r**2`)
    - `sqrt(x)`: raíz cuadrada
    
    **Funciones trigonométricas:**
    - `sin(theta)`, `cos(theta)`, `tan(theta)`
    
    **Funciones especiales:**
    - `exp(x)`: exponencial
    - `log(x)`: logaritmo natural
    - `pi`: constante π
    - `e`: constante e
    
    **Ejemplos:**
    - `r*z`: función lineal
    - `r**2*sin(theta)`: función cuadrática con componente angular
    - `r*exp(-z)`: función exponencial decreciente
    - `r*cos(theta)*z`: producto de componentes
    """)