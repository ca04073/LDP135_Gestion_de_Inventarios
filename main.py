from cli.app import iniciar_aplicacion

if __name__ == "__main__":
    try:
        iniciar_aplicacion()
    except KeyboardInterrupt:
        print("\n[!] Sistema cerrado.")