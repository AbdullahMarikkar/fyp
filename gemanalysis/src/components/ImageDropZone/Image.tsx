function Image({ image }: { image: any }) {
  return (
    <div>
      <img
        alt=""
        src={image.src}
        style={{
          height: "150px",
          width: "150px",
          marginRight: "15px",
          borderRadius: "30px",
        }}
      />
    </div>
  );
}
export default Image;
