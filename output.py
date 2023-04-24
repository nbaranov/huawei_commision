def log_commission(ip, header, result, output):
    with open(f"log/{ip}.md", "a", encoding="UTF-8") as md:
        if result == "OK":
            md.write(f'## * <span style="color:green"> {header} {result} </span> * \n\n')
        else:
            md.write(f'## * <span style="color:red"> {header} {result} </span> *\n\n')
        md.write(f" ' {output} ' \n\n")
        
    with open(f"log/{ip}.txt", "a", encoding="UTF-8") as txt:
        txt.write(f"\n\n {header} --- {result} \n\n {output}")