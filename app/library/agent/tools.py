from pkg.agent import tool

@tool
def search_employee(text: str) -> str:
    """
    Fungsi ini untuk kamu pakai jika ada yang bertanya terkait pegawai atau karyawan di perusahaan
    """
    if text == "iank":
        return "Iank adalah karyawan yang bekerja di perusahaan ini"
    
    return "Mohoh maaf saya tidak menemukan pegawai atas nama tersebut"

@tool
def get_assesment(text: str) -> str:
    """
    Fungsi ini untuk kamu pakai jika ada yang bertanya terkait penilaian karyawan di perusahaan
    """
    if text == "iank":
        return "Iank merupakan karyawan dengan nilai assesment 90, sangat baik dalam pekerjaannya"
    
    return "Mohoh maaf saya tidak menemukan penilaian atas nama tersebut"