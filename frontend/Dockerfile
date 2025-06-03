# Imagen base con Node.js
FROM node:20-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de configuración y dependencias
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto de los archivos del proyecto
COPY . .

# Expone el puerto que Vite usa por defecto (5173)
EXPOSE 5173

# Comando para desarrollo (hot-reload)
CMD ["npm", "run", "dev", "--", "--host"]
