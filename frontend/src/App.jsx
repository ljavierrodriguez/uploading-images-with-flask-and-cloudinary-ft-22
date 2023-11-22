import React, { useState } from 'react'

const App = () => {

  const [currentUser, setCurrentUser] = useState(null)

  const [name, setName] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const [avatar, setAvatar] = useState(null)
  const [cv, setCV] = useState(null)

  const [boletas, setBoletas] = useState([])

  const handleSubmit = (e) => {
    e.preventDefault();

    // creamos el objeto de tipo form
    const formData = new FormData()

    // añadimos campos al formulario
    formData.append("name", name)
    formData.append("username", username)
    formData.append("password", password)
    formData.append("avatar", avatar)
    formData.append("cv", cv)

    // si quiero subir varios archivos similares
    for(let i = 0; i < boletas.length; i++){
      formData.append("boletas", boletas[i])
    }


    // enviamos los datos a nuestra api para el registro del usuario
    register(formData)

    e.target.reset()

  }


  const register = async (datos) => {

    try {

      const response = await fetch('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        body: datos
      })

      const info = await response.json()

      if (info.msg) {
        console.log(info)
      } else {
        console.log(info)
        setCurrentUser(info)
        setName("")
        setUsername("")
        setPassword("")
        setAvatar(null)
        setCV(null)
      }

    } catch (error) {
      console.log(error.message)
    }

  }

  return (
    <>

      <form className='w-50 mx-auto my-5 p-4 bg-secondary text-white' onSubmit={handleSubmit}>

        <h5 className='text-center'>REGISTER</h5>
        <div className="form-group mb-3">
          <label htmlFor="name" className="form-label">Name</label>
          <input type="text" className="form-control" id="name" placeholder='ex: John Doe' onChange={e => setName(e.target.value)} />
        </div>

        <div className="form-group mb-3">
          <label htmlFor="username" className="form-label">Username</label>
          <input type="email" className="form-control" id="username" placeholder='ex: john.doe@gmail.com' onChange={e => setUsername(e.target.value)} />
        </div>

        <div className="form-group mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input type="password" className="form-control" id="password" placeholder='ex: *********' onChange={e => setPassword(e.target.value)} />
        </div>

        <div className="form-group mb-3">
          <label htmlFor="avatar" className="form-label">Avatar</label>
          <input type="file" id="avatar" className='form-control' onChange={e => setAvatar(e.target.files[0])} />
        </div>

        <div className="form-group mb-3">
          <label htmlFor="avatar" className="form-label">CV</label>
          <input type="file" id="cv" className='form-control' onChange={e => setCV(e.target.files[0])} />
        </div>

        <div className="form-group mb-3">
          <label htmlFor="boletas" className="form-label">Boletas</label>
          <input type="file" id="boletas" className='form-control' onChange={e => setBoletas(e.target.files)} multiple />
        </div>

        <button className="btn btn-primary btn-sm w-100 p-2 my-2">
          Register
        </button>
      </form>

      <div className="w-50 mx-auto p-5">
        {
          !!currentUser ?
          (
            <img src={currentUser?.user?.profile?.avatar !== "" ? currentUser?.user?.profile?.avatar : "https://picsum.photos/id/565/800/800"} alt="" className='img-fluid rounded-circle shadow avatar' />
          ):(
            <img src={"https://picsum.photos/id/565/800/800"} alt="" className='img-fluid rounded-circle shadow avatar' />
          )
        }
      </div>
    </>
  )
}

export default App