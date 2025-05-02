#!/bin/bash

echo "📦 Initialisiere Projekt mit npm..."
npm init -y

echo "📥 Installiere Abhängigkeiten..."
npm install fastify @fastify/swagger @fastify/swagger-ui @prisma/client

echo "📥 Installiere Dev-Abhängigkeiten..."
npm install -D typescript ts-node-dev prisma @types/node

echo "🛠️ Erstelle tsconfig.json..."
npx tsc --init --rootDir src --outDir dist --module ESNext --target ES2020 --esModuleInterop --moduleResolution Node --forceConsistentCasingInFileNames --strict --skipLibCheck

echo "📁 Erstelle Prisma Setup..."
npx prisma init

echo "✅ Fertig! Du kannst jetzt mit 'npm run dev' starten (nach dem Erstellen der scripts)."
