def split_triples_file(input_file, output_directory, chunk_size_mb):
    # Calculate the size of each chunk in bytes
    chunk_size_bytes = chunk_size_mb * 1024 * 1024

    # Read all triples from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        triples = f.readlines()

    # Initialize the current chunk size and chunk number
    current_chunk_size = 0
    current_chunk_number = 1

    # Initialize the current chunk
    current_chunk = ""

    # Loop through the triples
    for i, triple in enumerate(triples):
        # Add the triple to the current chunk
        current_chunk += triple

        # Update the current chunk size
        current_chunk_size += len(triple.encode('utf-8'))

        # If the current size exceeds the specified maximum, write the current chunk and start a new one
        if current_chunk_size >= chunk_size_bytes:
            current_chunk += "}"
            write_chunk(output_directory, current_chunk_number, current_chunk)
            current_chunk_number += 1

            # Reset current_chunk for the next chunk
            current_chunk = "<https://linkeddata.cultureelerfgoed.nl/graph/instanties-rce> {" if i < len(triples) - 1 else ""

            current_chunk_size = 0

    # Write the last chunk if there are remaining triples
    if current_chunk:
        write_chunk(output_directory, current_chunk_number, current_chunk)


def write_chunk(output_directory, chunk_number, content):
    output_file_path = f"{output_directory}/output_prefix{str(chunk_number).zfill(2)}.trig"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(content)

# Usage: Replace the paths and filename with your actual values
split_triples_file("/Users/patrickmout/Downloads/instanties-rce3.trig", "/Users/patrickmout/Downloads/LDV_RM", 120)
