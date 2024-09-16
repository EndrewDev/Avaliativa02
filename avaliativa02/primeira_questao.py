import os
import exifread

def get_exif_data(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        return tags

def get_lat_lon(tags):
    try:
        gps_latitude = tags['GPS GPSLatitude']
        gps_latitude_ref = tags['GPS GPSLatitudeRef']
        gps_longitude = tags['GPS GPSLongitude']
        gps_longitude_ref = tags['GPS GPSLongitudeRef']

        lat = [float(x.num) / float(x.den) for x in gps_latitude.values]
        lon = [float(x.num) / float(x.den) for x in gps_longitude.values]

        lat_ref = gps_latitude_ref.values
        lon_ref = gps_longitude_ref.values

        lat = lat[0] + lat[1] / 60 + lat[2] / 3600
        lon = lon[0] + lon[1] / 60 + lon[2] / 3600

        if lat_ref != "N":
            lat = -lat
        if lon_ref != "E":
            lon = -lon

        return lat, lon
    except KeyError:
        return None, None

def main():
    filename = input("Digite o nome da imagem (com extensão): ")
    if not os.path.isfile(filename):
        print("Arquivo não encontrado!")
        return

    with open(filename, 'rb') as f:
        file_start = f.read(4)
        if file_start.startswith(b'\xff\xd8\xff\xe1'):
            print(f"Arquivo JPEG encontrado: {filename}")
            tags = get_exif_data(filename)
            
            if tags:
                width = tags.get('EXIF ExifImageWidth', 'Desconhecido')
                height = tags.get('EXIF ExifImageLength', 'Desconhecido')
                camera_make = tags.get('Image Make', 'Desconhecido')
                camera_model = tags.get('Image Model', 'Desconhecido')
                capture_time = tags.get('EXIF DateTimeOriginal', 'Desconhecido')
                lat, lon = get_lat_lon(tags)
                city = 'Desconhecido'
                if lat and lon:
                    # Aqui você pode integrar com uma API de geocodificação para obter a cidade
                    pass

                print(f"Largura: {width}")
                print(f"Altura: {height}")
                print(f"Fabricante da Câmera: {camera_make}")
                print(f"Modelo da Câmera: {camera_model}")
                print(f"Data/Hora de Captura: {capture_time}")
                print(f"Latitude: {lat}")
                print(f"Longitude: {lon}")
                print(f"Cidade: {city}")

if __name__ == "__main__":
    main()


# import os
# import exifread

# def get_exif_data(file_path):
#     with open(file_path, 'rb') as f:
#         tags = exifread.process_file(f, stop_tag="UNDEF", details=False)
#         return tags

# def get_lat_lon(tags):
#     try:
#         gps_latitude = tags['GPS GPSLatitude']
#         gps_latitude_ref = tags['GPS GPSLatitudeRef']
#         gps_longitude = tags['GPS GPSLongitude']
#         gps_longitude_ref = tags['GPS GPSLongitudeRef']

#         lat = [float(x.num) / float(x.den) for x in gps_latitude.values]
#         lon = [float(x.num) / float(x.den) for x in gps_longitude.values]

#         lat_ref = gps_latitude_ref.values
#         lon_ref = gps_longitude_ref.values

#         lat = lat[0] + lat[1] / 60 + lat[2] / 3600
#         lon = lon[0] + lon[1] / 60 + lon[2] / 3600

#         if lat_ref != "N":
#             lat = -lat
#         if lon_ref != "E":
#             lon = -lon

#         return lat, lon
#     except KeyError:
#         return None, None

# def main():
#     filename = input("Digite o nome da imagem (com extensão): ")
#     if not os.path.isfile(filename):
#         print("Arquivo não encontrado!")
#         return

#     with open(filename, 'rb') as f:
#         file_start = f.read(4)
#         if file_start.startswith(b'\xff\xd8\xff\xe1'):
#             print(f"Arquivo JPEG encontrado: {filename}")
#             tags = get_exif_data(filename)
            
#             if tags:
#                 width = tags.get('EXIF ExifImageWidth', 'Desconhecido')
#                 height = tags.get('EXIF ExifImageLength', 'Desconhecido')
#                 camera_make = tags.get('Image Make', 'Desconhecido')
#                 camera_model = tags.get('Image Model', 'Desconhecido')
#                 capture_time = tags.get('EXIF DateTimeOriginal', 'Desconhecido')
#                 lat, lon = get_lat_lon(tags)
#                 city = 'Desconhecido'
#                 if lat and lon:
#                     # Aqui você pode integrar com uma API de geocodificação para obter a cidade
#                     pass

#                 print(f"Largura: {width}")
#                 print(f"Altura: {height}")
#                 print(f"Fabricante da Câmera: {camera_make}")
#                 print(f"Modelo da Câmera: {camera_model}")
#                 print(f"Data/Hora de Captura: {capture_time}")
#                 print(f"Latitude: {lat}")
#                 print(f"Longitude: {lon}")
#                 print(f"Cidade: {city}")
#             else:
#                 print("Nenhum dado EXIF encontrado.")
#         else:
#             print("O arquivo não é um JPEG válido com dados EXIF.")

# if __name__ == "__main__":
#     main()