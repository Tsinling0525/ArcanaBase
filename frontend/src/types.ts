export type Source = { source_id: string; kind: string; title: string; meta: any };
export type Hit = { score: number; chunk: { id: string; source_id: string; text: string; metadata: any } };
export type QueryResponse = { answer: string; hits: Hit[] };