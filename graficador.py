import matplotlib.pyplot as plt
import time

def run_graficador(q):
    plt.ion()
    fig, ax = plt.subplots()
    error_history = []

    FPS = 60  # Debe coincidir con el del simulador
    tiempo = 0

    while True:
        while not q.empty():
            (error, proportional_control,derivative_control,integral_control, neutron_target, realimentacion, perturbacion1, perturbacion2) = q.get()
            error_history.append((tiempo, error, proportional_control,derivative_control,integral_control, neutron_target, realimentacion, perturbacion1, perturbacion2))
            tiempo += 1 / FPS
            if len(error_history) > 3600:
                error_history.pop(0)


        times = [x[0] for x in error_history]
        errores = [x[1] for x in error_history]
        ctrl_proporcional = [x[2] for x in error_history]
        ctrl_derivativo = [x[3] for x in error_history]
        ctrl_integral = [x[4] for x in error_history]
        entrada = [x[5] for x in error_history]
        realimentacion = [x[6] for x in error_history]
        pert1 = [x[7] for x in error_history]
        pert2 = [x[8] for x in error_history]

        ax.clear()
        ax.plot(times, errores, label="Error")
        ax.plot(times, ctrl_proporcional, label="Controlador proporcional")
        ax.plot(times, ctrl_derivativo, label="Controlador derivativo")
        ax.plot(times, ctrl_integral, label="Controlador integral")
        ax.plot(times, entrada, label="Entrada (Setpoint)")
        ax.plot(times, realimentacion, label="Realimentación")
        ax.plot(times, pert1, label="Perturbación 1")
        ax.plot(times, pert2, label="Perturbación 2")
        ax.axhline(0, color="gray", linestyle="--")
        ax.set_ylim(-1000, 1000)
        ax.set_xlabel("Tiempo (s)")
        ax.legend()
        plt.pause(1 / FPS)
        time.sleep(1 / FPS)