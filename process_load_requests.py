from velocity_lim import velocity_limit_compiler
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type = str, help = 'path to the input file (i.e. input.txt)', required = True) 
    parser.add_argument("--output_path", type = str, help = 'path the output file will be (i.e. python_output.txt)', required = True) 
    
    args = parser.parse_args() 
    input_path = args.input_path
    output_path = args.output_path
    
    #Reads in the input path
    load_compiler = velocity_limit_compiler(input_txt_dir = input_path)
    
    #Outputs the load responses to the output path specified 
    load_compiler.output_to_text_file(output_path)