import matplotlib.pyplot as plt
import time

def run_graficador(q):
    plt.ion()
    fig, axs = plt.subplots(8, 1, figsize=(12, 16), sharex=True)
    manager = plt.get_current_fig_manager()
    manager.window.wm_geometry("+0+0")
    fig.tight_layout(pad=3.0)
    error_history = []

    FPS = 60  # Debe coincidir con el del simulador
    tiempo = 0

    while True:
        while not q.empty():
            (error, control, proportional_control, integral_control, derivative_control,
             neutron_target, realimentacion, perturbacion1, perturbacion2) = q.get()

            error_history.append((tiempo, error, control, proportional_control, integral_control,
                                  derivative_control, neutron_target, realimentacion,
                                  perturbacion1, perturbacion2))
            tiempo += 1 / FPS
            if len(error_history) > 1800:
                error_history.pop(0)

        # Extraer datos
        times = [x[0] for x in error_history]
        errores = [x[1] for x in error_history]
        control = [x[2] for x in error_history]
        ctrl_proporcional = [x[3] for x in error_history]
        ctrl_integral = [x[4] for x in error_history]
        ctrl_derivativo = [x[5] for x in error_history]
        entrada = [x[6] for x in error_history]
        realim = [x[7] for x in error_history]
        pert1 = [x[8] for x in error_history]
        pert2 = [x[9] for x in error_history]

        # Limpiar subgráficos
        for ax in axs:
            ax.clear()

        # Entrada
        axs[0].plot(times, entrada, label="Entrada (Setpoint)", color='purple')
        axs[0].axhline(0, color="gray", linestyle="--")
        axs[0].set_ylabel("Entrada")
        axs[0].legend()
        
        # Realimentacion
        axs[1].plot(times, realim, label="Realimentación", color='brown')
        axs[1].axhline(0, color="gray", linestyle="--")
        axs[1].set_ylabel("Señal")
        axs[1].legend()

        # Error
        axs[2].plot(times, errores, label="Error", color='red')
        axs[2].axhline(0, color="gray", linestyle="--")
        axs[2].set_ylabel("Error")
        axs[2].legend()

        # Controlador PID
        axs[3].plot(times, control, label="Control PID", color='black')
        axs[3].axhline(0, color="gray", linestyle="--")
        axs[3].set_ylabel("PID")
        axs[3].legend()

        # Proporcional
        axs[4].plot(times, ctrl_proporcional, label="Control Proporcional", color='blue')
        axs[4].axhline(0, color="gray", linestyle="--")
        axs[4].set_ylabel("P")
        axs[4].legend()

        # Gráfico 4: Integral
        axs[5].plot(times, ctrl_integral, label="Control Integral", color='orange')
        axs[5].axhline(0, color="gray", linestyle="--")
        axs[5].set_ylabel("I")
        axs[5].legend()

        # Derivativo
        axs[6].plot(times, ctrl_derivativo, label="Control Derivativo", color='green')
        axs[6].axhline(0, color="gray", linestyle="--")
        axs[6].set_ylabel("D")
        axs[6].legend()

        # Perturbaciones
        axs[7].plot(times, pert1, label="Perturbación 1", color='black')
        axs[7].plot(times, pert2, label="Perturbación 2", color='gray')
        axs[7].set_ylabel("Perturbaciones")
        axs[7].set_xlabel("Tiempo (s)")
        axs[7].legend()

        plt.pause(1 / FPS)
        time.sleep(1 / FPS)