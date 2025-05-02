// server.ts
import Fastify from 'fastify';
import swagger from '@fastify/swagger';
import swaggerUI from '@fastify/swagger-ui';
import { substanceRoutes } from './routes/substances';

const app = Fastify();

app.register(swagger, {
  openapi: {
    info: {
      title: 'Stoffdatenbank API',
      version: '1.0.0',
    },
  },
});

app.register(swaggerUI);

app.register(substanceRoutes, { prefix: '/substances' });

app.listen({ port: 3000 }, (err, address) => {
  if (err) throw err;
  console.log(`Server running at ${address}`);
});

// routes/substances.ts
import { FastifyInstance, FastifyPluginOptions } from 'fastify';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function substanceRoutes(server: FastifyInstance, options: FastifyPluginOptions) {
  server.get('/', async () => {
    return prisma.substance.findMany();
  });

  server.get('/:id', async (request) => {
    const { id } = request.params as { id: string };
    return prisma.substance.findUnique({ where: { id } });
  });

  server.post('/', async (request) => {
    const body = request.body as any;
    return prisma.substance.create({ data: body });
  });

  server.put('/:id', async (request) => {
    const { id } = request.params as { id: string };
    const body = request.body as any;
    return prisma.substance.update({ where: { id }, data: body });
  });

  server.delete('/:id', async (request) => {
    const { id } = request.params as { id: string };
    return prisma.substance.delete({ where: { id } });
  });
}

// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Substance {
  id           String   @id @default(uuid())
  name         String
  formula      String?
  casNumber    String?  @unique
  meltingPoint Float?
  boilingPoint Float?
  density      Float?
  category     String?
  createdAt    DateTime @default(now())
}
