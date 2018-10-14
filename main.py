if __name__ == "__main__":
    from gtfs_parsing import load_config
    from gtfs_parsing.analyses.analyses import run_analyses

    config = load_config.load_configuration()

    run_analyses(config)
