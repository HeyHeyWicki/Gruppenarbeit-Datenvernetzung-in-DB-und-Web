import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class PCUMotorMonitoring:
    def __init__(self):
        """
        Prädiktive Instandhaltung für Ricoh PCU Motoren
        Nidec Motor G4002105: DC 24V, 3.5A, 25W, 2500 RPM
        """
        self.motor_specs = {
            'spannung': 24,  # V
            'strom_normal': 6,  # A
            'leistung_normal': 30,  # W
            'drehzahl_normal': 2500,  # RPM
            'drehmoment_normal': 114.6  # mN·m
        }
        
        # Zeitstempel für Messungen
        self.timestamps = ['00:00', '00:15', '00:30', '00:45', '01:00', '01:15', '01:30', '01:45']
    
    def generate_normal_data(self):
        """Normale Betriebswerte - stabile Parameter"""
        return {
            'time': self.timestamps,
            'strom': [5.8, 5.9, 5.8, 6.0, 5.9, 5.8, 5.9, 6.0],
            'rpm': [2480, 2490, 2485, 2475, 2490, 2485, 2480, 2475],
            'drehmoment': [112, 114, 113, 115, 114, 113, 114, 115],
            'leistung': [29, 29.5, 29, 30, 29.5, 29, 29.5, 30]
        }
    
    def generate_blockierung_data(self):
        """Blockierung der PCU - plötzlicher Anstieg"""
        return {
            'time': self.timestamps,
            'strom': [5.8, 5.9, 6.0, 8.5, 9.2, 9.8, 10.1, 10.5],
            'rpm': [2480, 2490, 2485, 1850, 1650, 1580, 1520, 1480],
            'drehmoment': [112, 114, 115, 155, 168, 175, 180, 185],
            'leistung': [29, 29.5, 30, 42, 46, 48, 50, 52]
        }
    
    def generate_verschleiss_data(self):
        """Schleichender Verschleiß - kontinuierlicher Anstieg"""
        return {
            'time': self.timestamps,
            'strom': [5.8, 6.1, 6.3, 6.6, 6.9, 7.2, 7.5, 7.8],
            'rpm': [2480, 2465, 2450, 2435, 2420, 2405, 2390, 2375],
            'drehmoment': [112, 118, 122, 126, 130, 134, 138, 142],
            'leistung': [29, 31, 32, 33.5, 35, 36.5, 38, 39.5]
        }
    
    def generate_klemmung_data(self):
        """Intermittierende Klemmung - schwankende Werte"""
        return {
            'time': self.timestamps,
            'strom': [5.8, 7.2, 6.1, 8.1, 6.5, 8.8, 6.2, 9.1],
            'rpm': [2480, 2320, 2450, 2180, 2380, 2050, 2420, 1980],
            'drehmoment': [112, 135, 120, 148, 125, 162, 122, 168],
            'leistung': [29, 35, 31, 41, 33, 44, 32, 46]
        }
    
    def analyze_condition(self, data):
        """Analysiert den Zustand basierend auf Grenzwerten"""
        strom_avg = np.mean(data['strom'])
        rpm_avg = np.mean(data['rpm'])
        
        # Grenzwerte für Diagnose
        if strom_avg > 8.5 and rpm_avg < 1800:
            return "🔴 KRITISCH: Blockierung erkannt!"
        elif strom_avg > 7.0 and rpm_avg < 2400:
            return "🟡 WARNUNG: Verschleiß festgestellt"
        elif np.std(data['strom']) > 1.5:
            return "🟠 ACHTUNG: Intermittierende Klemmung"
        else:
            return "🟢 NORMAL: Betrieb im Sollbereich"
    
    def plot_monitoring_data(self, scenario='normal'):
        """Erstellt Monitoring-Diagramme für verschiedene Szenarien"""
        
        # Daten je nach Szenario laden
        data_functions = {
            'normal': self.generate_normal_data,
            'blockierung': self.generate_blockierung_data,
            'verschleiss': self.generate_verschleiss_data,
            'klemmung': self.generate_klemmung_data
        }
        
        data = data_functions[scenario]()
        condition = self.analyze_condition(data)
        
        # Deutsche Titel
        titles = {
            'normal': 'Normaler Betrieb',
            'blockierung': 'Blockierung der PCU',
            'verschleiss': 'Schleichender Verschleiß',
            'klemmung': 'Intermittierende Klemmung'
        }
        
        # Plot erstellen
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'PCU Motor Monitoring - {titles[scenario]}\n{condition}', 
                    fontsize=16, fontweight='bold')
        
        # Strom über Zeit
        ax1.plot(data['time'], data['strom'], 'b-o', linewidth=2, markersize=6)
        ax1.set_title('Stromaufnahme [A]', fontweight='bold')
        ax1.set_ylabel('Strom [A]')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=6.0, color='g', linestyle='--', alpha=0.7, label='Normal (6A)')
        ax1.axhline(y=8.5, color='r', linestyle='--', alpha=0.7, label='Kritisch (8.5A)')
        ax1.legend()
        
        # Drehzahl über Zeit
        ax2.plot(data['time'], data['rpm'], 'g-o', linewidth=2, markersize=6)
        ax2.set_title('Drehzahl [RPM]', fontweight='bold')
        ax2.set_ylabel('Drehzahl [RPM]')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=2500, color='g', linestyle='--', alpha=0.7, label='Soll (2500 RPM)')
        ax2.axhline(y=1800, color='r', linestyle='--', alpha=0.7, label='Kritisch (1800 RPM)')
        ax2.legend()
        
        # Drehmoment über Zeit
        ax3.plot(data['time'], data['drehmoment'], 'orange', marker='o', linewidth=2, markersize=6)
        ax3.set_title('Drehmoment [mN·m]', fontweight='bold')
        ax3.set_ylabel('Drehmoment [mN·m]')
        ax3.set_xlabel('Zeit')
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=114.6, color='g', linestyle='--', alpha=0.7, label='Normal (114.6 mN·m)')
        ax3.axhline(y=150, color='r', linestyle='--', alpha=0.7, label='Kritisch (150 mN·m)')
        ax3.legend()
        
        # Leistung über Zeit
        ax4.plot(data['time'], data['leistung'], 'purple', marker='o', linewidth=2, markersize=6)
        ax4.set_title('Leistungsaufnahme [W]', fontweight='bold')
        ax4.set_ylabel('Leistung [W]')
        ax4.set_xlabel('Zeit')
        ax4.grid(True, alpha=0.3)
        ax4.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Normal (30W)')
        ax4.axhline(y=40, color='r', linestyle='--', alpha=0.7, label='Kritisch (40W)')
        ax4.legend()
        
        # Layout optimieren
        plt.tight_layout()
        plt.subplots_adjust(top=0.93)
        
        return fig, data
    
    def generate_report(self, scenario='normal'):
        """Generiert einen Analysebericht für ARMS Integration"""
        data = getattr(self, f'generate_{scenario}_data')()
        condition = self.analyze_condition(data)
        
        report = f"""
=== PCU MOTOR MONITORING BERICHT ===
Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Motor: Nidec G4002105 (24V DC, 3.5A, 25W)

SZENARIO: {scenario.upper()}
STATUS: {condition}

MESSWERTE:
- Strom Ø: {np.mean(data['strom']):.1f}A (Bereich: {min(data['strom']):.1f}-{max(data['strom']):.1f}A)
- Drehzahl Ø: {np.mean(data['rpm']):.0f} RPM (Bereich: {min(data['rpm'])}-{max(data['rpm'])} RPM)
- Drehmoment Ø: {np.mean(data['drehmoment']):.1f} mN·m (Bereich: {min(data['drehmoment']):.1f}-{max(data['drehmoment']):.1f} mN·m)
- Leistung Ø: {np.mean(data['leistung']):.1f}W (Bereich: {min(data['leistung']):.1f}-{max(data['leistung']):.1f}W)

GRENZWERTÜBERSCHREITUNGEN:
"""
        
        # Grenzwertanalyse
        if max(data['strom']) > 8.5:
            report += f"⚠️  Strom kritisch: {max(data['strom']):.1f}A (>8.5A)\n"
        if min(data['rpm']) < 1800:
            report += f"⚠️  Drehzahl kritisch: {min(data['rpm'])} RPM (<1800 RPM)\n"
        if max(data['drehmoment']) > 150:
            report += f"⚠️  Drehmoment erhöht: {max(data['drehmoment']):.1f} mN·m (>150 mN·m)\n"
        if max(data['leistung']) > 40:
            report += f"⚠️  Leistung erhöht: {max(data['leistung']):.1f}W (>40W)\n"
        
        # Empfehlungen
        recommendations = {
            'normal': "✅ Normaler Betrieb - Keine Maßnahmen erforderlich",
            'blockierung': "🚨 SOFORT: Motor stoppen, PCU-Mechanik prüfen, Service-Techniker",
            'verschleiss': "🔧 GEPLANT: Wartungsintervall verkürzen, PCU-Austausch vorbereiten",
            'klemmung': "🔍 DIAGNOSE: Mechanische Führung und Schmierung prüfen"
        }
        
        report += f"\nEMPFEHLUNG:\n{recommendations.get(scenario, 'Unbekanntes Szenario')}\n"
        report += "\n=== ENDE BERICHT ===\n"
        
        return report

# Beispiel für die Verwendung
if __name__ == "__main__":
    # PCU Monitoring System initialisieren
    monitor = PCUMotorMonitoring()
    
    # Alle Szenarien durchlaufen
    scenarios = ['normal', 'blockierung', 'verschleiss', 'klemmung']
    
    for scenario in scenarios:
        print(f"\n{'='*50}")
        print(f"SZENARIO: {scenario.upper()}")
        print('='*50)
        
        # Diagramm erstellen
        fig, data = monitor.plot_monitoring_data(scenario)
        
        # Bericht generieren
        report = monitor.generate_report(scenario)
        print(report)
        
        # Diagramm anzeigen (optional auskommentieren für Batch-Verarbeitung)
        plt.show()
        
        # Als DataFrame für weitere Analyse
        df = pd.DataFrame(data)
        print("ROHDATEN:")
        print(df.to_string(index=False))
        print("\nSTATISTIK:")
        print(df.describe())
