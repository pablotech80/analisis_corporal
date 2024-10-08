from datetime import datetime
import math
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Cliente, Base


'''Configuración de la base de datos'''

engine = create_engine('sqlite:///clientes.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def calcular_tmb(peso, altura, edad, genero):

    """Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Harris-Benedict.

        Args:
            peso (float): Peso del usuario en kilogramos.
            altura (float): Altura del usuario en centímetros.
            edad (int): Edad del usuario en años.
            genero (str): Género del usuario ('h' para hombre, 'm' para mujer).

        Returns:
            float: La TMB calculada
        """
    if genero == 'h':
            tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    else:
            tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)
    return tmb

def calcular_imc(peso, altura):

    """Calcula el Índice de Masa Corporal (IMC).

        Args:
            peso (float): Peso del usuario en kilogramos.
            altura (float): Altura del usuario en centímetros.

        Returns:
            float: El IMC calculado.
        """
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    return imc

def interpretar_imc(imc, ffmi, genero):

    """Interpreta el resultado del IMC considerando el FFMI.

        Args:
            imc (float): Índice de Masa Corporal calculado.
            ffmi (float): Índice de Masa Libre de Grasa.
            genero (str): Género del usuario.

        Returns:
            str: Interpretación del IMC basada en los valores de FFMI y género.
        """
    if imc > 25 and ffmi > 19 if genero == 'm' else ffmi > 16:
        return "El IMC es alto, pero puede estar influenciado por una alta masa muscular."
    elif imc < 18.5:
        return "El IMC es bajo, se recomienda consultar con un profesional de salud."
    else:
        return "El IMC está dentro del rango normal."

def calcular_porcentaje_grasa(cintura, cadera, cuello, altura, genero):

    """Calcula el porcentaje de grasa corporal usando la fórmula de la Marina Estadounidense.

        Args:
            cintura (float): Medida de la cintura en centímetros.
            cadera (float): Medida de la cadera en centímetros.
            cuello (float): Medida del cuello en centímetros.
            altura (float): Altura en centímetros.
            genero (str): Género del usuario ('h' para hombre, 'm' para mujer).

        Returns:
            float: El porcentaje de grasa corporal calculado.
        """
    if genero == 'h':
            porcentaje_grasa = 495 / (
                        1.0324 - 0.19077 * math.log10(cintura - cuello) + 0.15456 * math.log10(altura)) - 450
    else:
            porcentaje_grasa = 495 / (
                        1.29579 - 0.35004 * math.log10(cintura + cadera - cuello) + 0.22100 * math.log10(altura)) - 450
    return porcentaje_grasa

def interpretar_porcentaje_grasa(porcentaje_grasa, genero):

    """
        Interpreta el porcentaje de grasa corporal basándose en el género y proporciona una evaluación cualitativa.

        Args:
            porcentaje_grasa (float): El porcentaje de grasa corporal calculado.
            genero (str): El género del individuo ('h' para hombres, 'm' para mujeres).

        Returns:
            str: Una cadena de texto que describe el estado del porcentaje de grasa corporal en términos de salud.
        """
    if genero == 'h':
        if porcentaje_grasa > 25:
            return "Alto"
        elif porcentaje_grasa < 6:
            return "Bajo"
        else:
            return "Normal"
    else:
        if porcentaje_grasa > 32:
            return "Alto"
        elif porcentaje_grasa < 16:
            return "Bajo"
        else:
            return "Normal"

def calcular_agua_total(peso, altura, edad, genero):

    """Calcula el agua total del cuerpo usando una fórmula simplificada.

        Args:
            peso (float): Peso del usuario en kilogramos.
            altura (float): Altura del usuario en centímetros.
            edad (int): Edad del usuario en años.
            genero (str): Género del usuario ('h' para hombre, 'm' para mujer).

        Returns:
            float: El total de agua en el cuerpo calculado.
        """
    if genero == 'h':
            agua_total = 2.447 - (0.09156 * edad) + (0.1074 * altura) + (0.3362 * peso)
    else:
            agua_total = -2.097 + (0.1069 * altura) + (0.2466 * peso)
    return agua_total


def calcular_peso_saludable(altura):

    """Calcula el rango de peso saludable basado en la altura utilizando el rango de IMC saludable.

        Args:
            altura (float): Altura del usuario en centímetros.

        Returns:
            tuple: Peso mínimo y máximo dentro del rango de IMC saludable.
        """
    altura_m = altura / 100
    peso_min = 18.5 * (altura_m ** 2)
    peso_max = 24.9 * (altura_m ** 2)
    return peso_min, peso_max

def calcular_peso_min(altura):

    """Calcula el peso mínimo saludable basado en la altura y el IMC mínimo saludable.

        Args:
            altura (float): Altura del usuario en centímetros.

        Returns:
            float: Peso mínimo saludable.
        """
    altura_m = altura / 100
    peso_min = 18.5 * (altura_m ** 2)
    return peso_min

def calcular_peso_max(altura):

    """Calcula el peso máximo saludable basado en la altura y el IMC máximo saludable.

        Args:
            altura (float): Altura del usuario en centímetros.

        Returns:
            float: Peso máximo saludable.
        """
    altura_m = altura / 100
    peso_max = 24.9 * (altura_m ** 2)
    return peso_max

def calcular_sobrepeso(peso, altura):

    """Calcula el sobrepeso comparando el peso actual con el peso máximo saludable.

        Args:
            peso (float): Peso actual del usuario en kilogramos.
            altura (float): Altura del usuario en centímetros.

        Returns:
            float: Sobrepeso calculado, si lo hay.
        """
    peso_max = calcular_peso_max(altura)
    sobrepeso = max(0, peso - peso_max)
    return sobrepeso

def calcular_masa_muscular(peso, porcentaje_grasa):

    """
        Calcula la masa muscular (masa magra) del cuerpo descontando el porcentaje de grasa.

        Args:
            peso (float): Peso total del usuario en kilogramos.
            porcentaje_grasa (float): Porcentaje de grasa corporal del usuario.

        Returns:
            float: Masa muscular calculada en kilogramos.
        """
    masa_muscular = peso * ((100 - porcentaje_grasa) / 100)
    return masa_muscular

def calcular_ffmi(masa_muscular, altura):

    """
        Calcula el Índice de Masa Libre de Grasa (FFMI, por sus siglas en inglés).

        Args:
            masa_muscular (float): Masa muscular del usuario en kilogramos.
            altura (float): Altura del usuario en centímetros.

        Returns:
            float: El FFMI calculado basado en la masa muscular y la altura.
        """
    altura_m = altura / 100
    ffmi = masa_muscular / (altura_m ** 2)
    return ffmi

def interpretar_ffmi(ffmi, genero):

    """
        Proporciona una interpretación del FFMI basado en rangos preestablecidos que varían según el género,
        aparte da información sobre los mín y máx de potencial genético según los valores, dando así un
        número superior al máx, uso de fármacos para lograr ese resultado.

        Args:
            ffmi (float): Valor del FFMI a interpretar.
            genero (str): Género del usuario ('h' para hombres, 'm' para mujeres).

        Returns:
            str: Descripción del nivel de forma física basado en el FFMI.
        """
    if genero == 'h':
        if ffmi < 18:
            return "Lejos del máximo potencial (pobre forma física)"
        elif 18 <= ffmi < 19:
            return "Cercano a la normalidad"
        elif 19 <= ffmi < 20:
            return "Normal"
        elif 20 <= ffmi < 21:
            return "Superior a la normalidad (buena forma física)"
        elif 21 <= ffmi < 22.5:
            return "Fuerte (Muy buena forma física)"
        elif 22.5 <= ffmi < 24:
            return "Muy fuerte (Excelente forma física). Cerca del máximo potencial."
        elif 24 <= ffmi < 25.5:
            return "Muy cerca del máximo potencial."
        elif 25.5 <= ffmi < 27:
            return "Potencial máximo natural alcanzado. Muy muy pocos llegan naturales"
        elif 27 <= ffmi < 29:
            return "Prácticamente imposible sin fármacos"
        else:
            return "Imposible sin fármacos"
    else:
        if ffmi < 13.5:
            return "Lejos del máximo potencial (pobre forma física)"
        elif 13.5 <= ffmi < 14.5:
            return "Cercano a la normalidad"
        elif 14.5 <= ffmi < 16:
            return "Normal"
        elif 16 <= ffmi < 17:
            return "Superior a la normalidad (buena forma física)"
        elif 17 <= ffmi < 18.5:
            return "Fuerte (Muy buena forma física)"
        elif 18.5 <= ffmi < 20:
            return "Muy fuerte (Excelente forma física). Cerca del máximo potencial."
        elif 20 <= ffmi < 21:
            return "Muy cerca del máximo potencial."
        elif 21 <= ffmi < 22:
            return "Potencial máximo natural alcanzado. Muy muy pocos llegan naturales"
        elif 22 <= ffmi < 23:
            return "Prácticamente imposible sin fármacos"
        else:
            return "Imposible sin fármacos"

def calcular_rcc(cintura, cadera):

    """Calcula la relación cintura-cadera, un indicador de distribución de grasa corporal en la zona abdominal

        Args:
            cintura (float): Medida de la cintura en centímetros.
            cadera (float): Medida de la cadera en centímetros.

        Returns:
            float: Relación cintura-cadera calculada.
        """
    if cadera == 0:
        return 0
    rcc = cintura / cadera
    return rcc

def calcular_relacion_cintura_cadera(cintura, cadera):
    """
        Calcula la relación cintura-cadera (RCC), que es un indicador de la distribución de la grasa corporal.

        Args:
            cintura (float): Medida de la cintura en centímetros.
            cadera (float): Medida de la cadera en centímetros.

        Returns:
            float: La relación cintura-cadera calculada.
        """

    return cintura / cadera

def interpretar_rcc(rcc, genero):

    """Interpreta la relación cintura-cadera basándose en umbrales específicos de riesgo según el género,
        con este dato se sabe que nivel de sobrepeso tiene y si proviene de hipertrofia muscular o acumulación de grasa.

        Args:
            rcc (float): Relación cintura-cadera calculada.
            genero (str): Género del usuario ('h' para hombre, 'm' para mujer).

        Returns:
            str: Interpretación del nivel de riesgo asociado con la RCC.
        """
    if genero == 'h':
        if rcc > 0.95:
            return "Alto riesgo"
        elif 0.90 < rcc <= 0.95:
            return "Moderado riesgo"
        else:
            return "Bajo riesgo"
    else:
        if rcc > 0.85:
            return "Alto riesgo"
        elif 0.80 < rcc <= 0.85:
            return "Moderado riesgo"
        else:
            return "Bajo riesgo"

def calcular_ratio_cintura_altura(cintura, altura):

    """Calcula el ratio cintura-altura, un indicador de riesgo de salud metabólica.

        Args:
            cintura (float): Medida de la cintura en centímetros.
            altura (float): Altura del usuario en centímetros.

        Returns:
            float: Ratio cintura-altura calculado.
        """
    return cintura / altura

def interpretar_ratio_cintura_altura(ratio):

    """Interpreta el ratio cintura-altura para evaluar el riesgo metabólico
        y posibles riesgos cardiovasculares

        Args:
            ratio (float): Ratio cintura-altura calculado.

        Returns:
            str: Interpretación del nivel de riesgo metabólico basado en el ratio.
        """
    if ratio >= 0.6:
        return "Alto riesgo"
    elif 0.5 <= ratio < 0.6:
        return "Moderado riesgo"
    else:
        return "Bajo riesgo"

def calcular_calorias_diarias(tmb, objetivo):

    """Calcula las calorías diarias necesarias basadas en la TMB y el objetivo nutricional.

        Args:
            tmb (float): Tasa Metabólica Basal calculada.
            objetivo (str): Objetivo nutricional ('mantener', 'perder', 'ganar').

        Returns:
            float: Calorías diarias ajustadas según el objetivo.
        """

    if objetivo == 'mantener':
        return tmb * 1.2  # Factor de actividad moderado
    elif objetivo == 'perder':
        return tmb * 1.2 * 0.8  # 20% de reducción calórica
    elif objetivo == 'ganar':
        return tmb * 1.2 * 1.2  # 20% de aumento calórico

def calcular_macronutrientes(calorias, objetivo):

    """Calcula la distribución de macronutrientes basada en las calorías diarias y el objetivo nutricional,
        con esta información distribuimos en un marco estandar la cantidad necesaria según objetivo de macros para
        formalizar un plan de dieta base.

        Args:
            calorias (float): Calorías diarias recomendadas.
            objetivo (str): Objetivo nutricional ('mantener', 'perder', 'ganar').

        Returns:
            tuple: Gramos de proteínas, carbohidratos y grasas recomendados diariamente.
        """
    if objetivo == 'mantener':
        proteinas = (calorias * 0.30) / 4
        carbohidratos = (calorias * 0.40) / 4
        grasas = (calorias * 0.30) / 9
    elif objetivo == 'perder':
        proteinas = (calorias * 0.40) / 4
        carbohidratos = (calorias * 0.40) / 4
        grasas = (calorias * 0.20) / 9
    elif objetivo == 'ganar':
        proteinas = (calorias * 0.30) / 4
        carbohidratos = (calorias * 0.50) / 4
        grasas = (calorias * 0.20) / 9
    return float(proteinas), float(carbohidratos), float(grasas)


def guardar_datos(cliente_data):
    """
        Guarda los datos del cliente en la base de datos. Asegura que todos los campos necesarios estén presentes y sean válidos.

        Args:
            cliente_data (dict): Un diccionario con todos los datos del cliente, incluyendo nombre, medidas corporales, y resultados de cálculos.

        Returns:
            bool: True si los datos se guardaron correctamente, False si ocurrió un error.
        """

    try:
        cliente = Cliente(
            nombre=cliente_data['nombre'],
            fecha=cliente_data['fecha'],
            peso=cliente_data['peso'],
            altura=cliente_data['altura'],
            edad=cliente_data['edad'],
            genero=cliente_data['genero'],
            cintura=cliente_data['cintura'],
            cadera=cliente_data['cadera'],
            cuello=cliente_data['cuello'],
            tmb=cliente_data['tmb'],
            porcentaje_grasa=cliente_data['porcentaje_grasa'],
            peso_grasa=cliente_data['peso_grasa'],
            masa_muscular=cliente_data['masa_muscular'],
            agua_total=cliente_data['agua_total'],
            ffmi=cliente_data['ffmi'],
            peso_min=cliente_data['peso_min'],
            peso_max=cliente_data['peso_max'],
            sobrepeso=cliente_data['sobrepeso'],
            rcc=cliente_data['rcc'],
            ratio_cintura_altura=cliente_data['ratio_cintura_altura'],
            calorias_diarias=cliente_data['calorias_diarias'],
            proteinas=cliente_data['proteinas'],
            carbohidratos=cliente_data['carbohidratos'],
            grasas=cliente_data['grasas']
        )
        session.add(cliente)
        session.commit()
        print("Datos guardados exitosamente.")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error al guardar datos: {e}")
        return False

def recuperar_historial():

    """
            Recupera el historial completo de clientes de la base de datos.

            Returns:
                list: Una lista de objetos Cliente, cada uno representando un registro histórico de un cliente.
            """
    try:
        return session.query(Cliente).all()
    except Exception as e:
        print(f"Error al recuperar historial: {e}")
        return []
