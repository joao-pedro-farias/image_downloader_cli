#!/usr/bin/env python3
import asyncio
import aiohttp
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

class ImageDownloader:
    def __init__(self, download_dir=None):
        if download_dir:
            self.download_dir = Path(download_dir)
        else:
            self.download_dir = Path.home() / "Pictures" / "imgdown_downloads"
        
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    async def download_image(self, session, url):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    
                    # Verifica se é imagem
                    content_type = response.headers.get('content-type', '')
                    if not content_type.startswith('image/'):
                        return f"❌ Não é imagem: {url}"
                    
                    # Nome único
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    
                    # Extensão inteligente
                    if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        ext = Path(url).suffix.lower()
                    else:
                        # Tenta adivinhar pelo content-type
                        if 'png' in content_type:
                            ext = '.png'
                        elif 'jpeg' in content_type or 'jpg' in content_type:
                            ext = '.jpg'
                        elif 'gif' in content_type:
                            ext = '.gif'
                        elif 'webp' in content_type:
                            ext = '.webp'
                        else:
                            ext = '.jpg'
                    
                    filename = f"img_{timestamp}{ext}"
                    filepath = self.download_dir / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    
                    return f"✅ {filename}"
                else:
                    return f"❌ HTTP {response.status}: {url}"
        except Exception as e:
            return f"❌ Erro: {url} - {str(e)}"
    
    async def download_all(self, urls, max_concurrent=5):
        print(f"📥 Baixando {len(urls)} imagens...")
        print(f"📁 Pasta: {self.download_dir}")
        print("-" * 50)
        
        # Limita conexões simultâneas
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = self.download_with_semaphore(session, url, semaphore)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            
            for result in results:
                print(result)
        
        print("🎉 Download finalizado!")
    
    async def download_with_semaphore(self, session, url, semaphore):
        async with semaphore:
            return await self.download_image(session, url)

def read_urls_from_file(filename):
    """Lê URLs de arquivo"""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def main():
    parser = argparse.ArgumentParser(description='Async Image Downloader')
    parser.add_argument('urls', nargs='*', help='URLs para download')
    parser.add_argument('-f', '--file', help='Arquivo com URLs')
    parser.add_argument('-o', '--output', help='Pasta de destino')
    parser.add_argument('-c', '--concurrent', type=int, default=5, 
                       help='Downloads simultâneos (padrão: 5)')
    
    args = parser.parse_args()
    
    # Coleta URLs
    all_urls = []
    
    if args.file:
        try:
            urls_from_file = read_urls_from_file(args.file)
            all_urls.extend(urls_from_file)
            print(f"📄 Lidas {len(urls_from_file)} URLs de {args.file}")
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {args.file}")
            return
    
    if args.urls:
        all_urls.extend(args.urls)
        print(f"🔗 Adicionadas {len(args.urls)} URLs diretas")
    
    if not all_urls:
        print("❌ Nenhuma URL fornecida")
        parser.print_help()
        return
    
    # Remove duplicatas
    unique_urls = list(set(all_urls))
    if len(unique_urls) < len(all_urls):
        print(f"🔄 Removidas {len(all_urls) - len(unique_urls)} URLs duplicadas")
    
    # Executa download
    downloader = ImageDownloader(args.output)
    asyncio.run(downloader.download_all(unique_urls, args.concurrent))

if __name__ == "__main__":
    main()
