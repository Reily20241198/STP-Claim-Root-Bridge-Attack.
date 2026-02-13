# Ataque STP Claim Root Bridge  
## Documentación Técnica Profesional
ENLACE DEL VIDEO: https://www.youtube.com/watch?v=2by5Jxheums


## Aviso Legal

Este proyecto ha sido desarrollado **exclusivamente con fines educativos y de auditoría de seguridad autorizada**.  
El uso de esta herramienta en redes, sistemas o infraestructuras **sin autorización expresa** es ilegal y puede acarrear consecuencias legales.

El autor no se hace responsable del uso indebido de la información o del código presentado.

---

## 1. Descripción General

El **STP Claim Root Bridge Attack** es un ataque de capa 2 que explota el funcionamiento del **Spanning Tree Protocol (STP)**.  
El atacante envía **BPDUs falsificados** anunciándose como el **Root Bridge** de la red, utilizando una prioridad STP más baja que la de los switches legítimos.

Como resultado, la topología de la red se reorganiza y el atacante puede posicionarse en el centro del tráfico de red.

Este ataque puede permitir:
- Man-in-the-Middle (MitM)
- Intercepción de tráfico
- Degradación del rendimiento de la red
- Denegación de servicio (DoS)

---

## 2. Objetivo del Script

El objetivo del script es **demostrar de forma práctica cómo un atacante puede reclamar el rol de Root Bridge** en una red con STP mal configurado.

Este laboratorio permite:
- Comprender el funcionamiento interno de STP
- Analizar el impacto de BPDUs maliciosas
- Evaluar riesgos en redes sin protecciones de capa 2
- Aplicar medidas de mitigación adecuadas

Este proyecto está destinado únicamente a **laboratorios académicos y pruebas de seguridad autorizadas**.

---

## 3. Topología de Red

La práctica se realiza sobre una red LAN con switches interconectados mediante STP.

| Dispositivo | Descripción |
|------------|-------------|
| Switch legítimo | Root Bridge original |
| Switch secundario | Switch de acceso |
| Atacante | Kali Linux enviando BPDUs falsas |
| Hosts | Dispositivos finales conectados |

**Protocolo utilizado:** Spanning Tree Protocol (STP)

---

## 4. Parámetros Utilizados

- Interfaz de red: `eth0`
- Prioridad STP falsa: `0`
- Intervalo de envío de BPDUs
- Modo de ataque: continuo

---

## 5. Requisitos para Utilizar la Herramienta

### Requisitos de Software
- Sistema operativo Linux (Kali Linux recomendado)
- Python 3.x
- Librería Scapy

### Requisitos del Sistema
- Permisos de superusuario (root o sudo)
- Acceso a una red con STP habilitado

### Instalación de dependencias
```bash
sudo apt update
sudo apt install python3-scapy -y
```

---

## 6. Evidencias y Capturas de Pantalla

Las evidencias del laboratorio deben almacenarse en el siguiente directorio:

Esta es mi topologia sencilla
<img width="1312" height="654" alt="Screenshot_18" src="https://github.com/user-attachments/assets/5e62f543-7e7d-4f7d-9bd2-db8b2b6bbb93" />
lo siguiente sera ver el estado del SW
<img width="889" height="496" alt="Screenshot_16" src="https://github.com/user-attachments/assets/f8bbd9da-ef4c-420c-b447-4bbe4a7a4262" />
Como pudimos ver el root lo tiene lo que es la E0/1 y queremos que la tenga la E0/3
que ese es el del atacante 
<img width="1034" height="857" alt="Screenshot_15" src="https://github.com/user-attachments/assets/29872e0a-0697-4e9f-800f-de41bd68f4e0" />
ya aqui procedemos a realizar nuestro script corriendo y una vez que ya lo tengamos corriendo vamoos a ir para el sw a ver si es el del root
<img width="730" height="292" alt="Screenshot_17" src="https://github.com/user-attachments/assets/4ca5fc45-4220-4a06-ab14-f332e12511f2" />
Ejectivamente ya es el root 

## 7. Medidas de Mitigación

Para prevenir ataques de **STP Claim Root Bridge**, se recomiendan las siguientes medidas:

- Habilitar **BPDU Guard** en puertos de acceso
- Utilizar **Root Guard** en puertos críticos
- Definir manualmente el Root Bridge
- Segmentar la red correctamente
- Monitorear eventos STP

### Ejemplo de configuración en Cisco IOS
```bash
spanning-tree portfast bpduguard default
spanning-tree guard root
```

---

## 8. Uso Ético

Esta herramienta debe utilizarse **únicamente** para:
- Prácticas académicas
- Laboratorios de ciberseguridad
- Auditorías de seguridad con autorización

🚫 Está estrictamente prohibido su uso en:
- Redes productivas
- Redes públicas
- Sistemas sin consentimiento del propietario

---

## 9. Autor

Reily Castillo Del Rosario  
Estudiante de Seguridad de informatica  
República Dominicana  

---

## 10. Contribuciones

Las contribuciones son bienvenidas siempre que:
- Mantengan un enfoque educativo
- No promuevan actividades ilegales
- Incluyan documentación clara y profesional

Proceso de contribución:
1. Realizar un fork del repositorio
2. Crear una nueva rama
3. Enviar un Pull Request debidamente documentado

---

## 11. Licencia

Este proyecto se distribuye bajo la licencia **MIT**, permitiendo su uso, modificación y distribución con fines educativos, siempre que se mantenga la atribución correspondiente al autor.
