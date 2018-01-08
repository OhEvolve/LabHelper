
Author: Patrick V. Holec


LabHelper is a interactive shell for designing lab experiments,scheduling tasks,etc.


Reach out to Michael to decide if worthwhile
Talk to Jonathan to see if he would be interested
Talk to Brooke to see if he would be interested

--------
Outline:
--------

~/[home]
    main.py - Main callable method
    test.py - Workshop for ideas/methods
    update.py - Updates available database methods

~/sequences/ (folder for plasmids/sequences/genes)
    format:
        Description: (text)
        Species: (comma separated text)
        Author: (text)
        Tags: (comma seperated text)
        Sequence: (text)

~/database/ (folder for accumulated information)
    elements/ [regions of DNA that correspond to certain functions]
        Format:
            Type: str - DNA, Protein
            Sequence: str - DNA, protein sequence, written either as:
                ATCATCGTGTATC
                ATCA...ATC
            Shorthand: str - label for charts
            Description: str - description of element
            Citation: str - url of link to source
            
    species/
        Format:
            Alternative: (comma seperated text)
            Description: (text)
            
    codons/
        Format:
            Species: (comma seperated text)
            # TODO: find standard way to input these


    protocols/ 
        protocol_name/ 
            protocol.py
                python script, main methods - 
                    > (name1)
                    > (name2)
            optimize.py
                python script, uses a collection of methods to suggest edits to protocol

    reactions/

    reagents/
        Format:
            Label: (comma seperated text) DNA polymerase, RNA polymerase
            Notes: 
            Speed: 1kB

        dna_polymerase/
            Template: ssDNA,ssDNA primer
            Generates: dsDNA

        restriction_enzymes/
            Format:
                Sequence: ATCCTA
                Site: tuple - None (internal), or (2/4) 
                Description: str - optional
                Citation: str - url of link to source

    optimize/
        optimize_name/
            python script, for optimizing from certain inputs
            optimizer.py
            (aux. files if needed)
        -- codon_usage.py
        -- tm_optimizer.py

~/logs/ 
    commands.txt 
        # append upwards?
    experiments.txt
        # append upwards?
    schedule.txt

~/visuals/
    sequence.py
        python script that visualizes stuff
    database.py
        python script for exploring database

