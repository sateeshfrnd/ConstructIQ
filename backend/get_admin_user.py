from core.security import hash_password, verify_password


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


password = "admin123"   # change this
hashed = pwd_context.hash(password)

print(hashed)
print(verify_password(password, hashed))

mashed1= hash_password("admin123")
print(mashed1)

print(verify_password(password, mashed1))