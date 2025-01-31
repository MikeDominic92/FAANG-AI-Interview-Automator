Add-Type -AssemblyName System.Drawing

# Create a new bitmap
$bitmap = New-Object System.Drawing.Bitmap(64, 64)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)

# Set background
$graphics.Clear([System.Drawing.Color]::FromArgb(0, 120, 212))

# Draw text
$font = New-Object System.Drawing.Font("Arial", 24, [System.Drawing.FontStyle]::Bold)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$graphics.DrawString("AI", $font, $brush, 12, 12)

# Save as icon
$bitmap.Save("icon.png", [System.Drawing.Imaging.ImageFormat]::Png)

# Convert to ICO using ImageMagick
magick convert icon.png icon.ico
