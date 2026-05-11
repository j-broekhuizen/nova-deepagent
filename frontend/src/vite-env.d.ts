/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_LANGGRAPH_PORT?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
