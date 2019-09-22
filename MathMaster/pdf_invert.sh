#!/usr/bin/env bash

bin_dir="{1:-C:\Users\guzma\Downloads\PortableInstallations\texlive\tlpkg\tlgs\bin\gswin32c.exe}"
echo "Enter input directory: " && read in_dir
out_dir="${in_dir}/inverted"

cd "${in_dir}" && (mkdir "${out_dir}" || echo "Could not make a new directory (${out_dir})")
ls . | grep -E "\.pdf$" | \
  xargs -I{} "${bin_dir}" \
    -o "${out_dir}/{}" -sDEVICE=pdfwrite \
    -c "{1 exch sub}{1 exch sub}{1 exch sub}{1 exch sub} setcolortransfer" -f "{}"
echo "Press enter to continue: " && read
