# CNC Plotter Software Architecture & Flow Diagram

This document outlines the software flow of the CNC Controller project, from user input to physical motor movement.

## 1. High-Level Flow Diagram (Mermaid)

```mermaid
graph TD
    %% User Layer
    User((User)) -->|Telegram Message| Bot[Telegram Bot Interface]

    %% Orchestration Layer (main_auto.py)
    subgraph Python_Controller [Main Controller - main_auto.py]
        Bot -->|Text Input| NLP[NLP Pipeline]
        
        subgraph NLP_Pipeline [NLP Parser]
            NLP -->|Match?| Preset[Preset Lookup]
            Preset -->|No| Regex[Regex Parser]
            Regex -->|No| Ollama[Ollama LLM - Qwen2.5]
        end

        NLP_Pipeline -->|Parametric Equations| Math[Math Evaluator - NumPy]
        Math -->|Raw X,Y Arrays| Queue((Draw Queue))
    end

    %% Execution Layer
    subgraph Execution_Thread [Main Thread Loop]
        Queue -->|Next Job| Solution[Solution Logic]
        
        subgraph Scaling_Logic [Coordinate Transformation]
            Solution -->|Scale 1/16| S1[Micro-Precision Scaling]
            S1 -->|Clip 0.0-6.0| S2[Boundary Clipping]
            S2 -->|Shift| S3[Positive Origin Alignment]
        end

        S3 -->|Final Coords| Serial[Serial Dispatcher]
        S3 -->|Visual Feedback| Tkinter[Tkinter Simulator]
        S3 -->|Memory| Header[C Header Export - Custom.h]
    end

    %% Hardware Layer
    Serial -->|G-Code: G1 X... Y... S...| ESP32[ESP32 Controller - CNC_Controller_V2.ino]

    subgraph ESP32_Firmware [Firmware Logic]
        ESP32 -->|Parse| GCode[G-Code Parser]
        GCode -->|Calculated Time| Motor[Motor Controller]
        
        subgraph Motor_Logic [Servo Control]
            Motor -->|Low Freq 30Hz| PWM[PWM Pulse Generation]
            PWM -->|Power Cap 25/88| MG996R[MG996R Servos]
        end
        
        Motor -->|Movement Done| OK[Send 'OK' to Python]
    end

    OK -.->|Flow Control| Serial
```

## 2. Detailed Software Components

### A. NLP Pipeline (Input Interpretation)
- **Preset Lookup**: Checks if the user typed a known shape name (e.g., "heart", "circle").
- **Regex Parser**: Handles direct mathematical equations (e.g., `y = sin(x)`).
- **Ollama (Qwen2.5)**: Uses local LLM to interpret complex natural language requests and convert them into JSON parametric equations.

### B. Coordinate Transformation (Precision Layer)
- **1/16 Scaling**: All input units are divided by 16 for micro-drawings.
- **Safety Clipping**: Forcefully limits coordinates to a `[0.0, 6.0]` range.
- **Center Alignment**: Automatically shifts shapes to fit within the active zone.

### C. Serial Communication (G-Code)
- **Baud Rate**: 115200 bps.
- **Protocol**: Custom simplified G-code (`G1 X... Y... S...`).
- **Synchronization**: Uses a "Wait-for-OK" handshake to ensure the hardware doesn't get overwhelmed.

### D. Hardware Control (ESP32 Firmware)
- **Low Frequency Mode**: 30Hz PWM prevents mechanical resonance in MG996R servos.
- **Velocity Management**: Proportional power calculation for straight-line diagonal moves.
- **Power Limiting**: Caps servo duty cycle swing to 25 (out of 88) for stability with large 6.7cm wheels.
