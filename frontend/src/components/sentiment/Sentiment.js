import React from 'react'

const Sentiment = ({data}) => {
    let color = data.prediction == 0 ? "success" : "danger"
    return (
        <div className="container justify-content-center">
            <h3 className="text-center">
                <i className={`fas fa-${data.prediction == 0 ? "thumbs-up": "thumbs-down"
                } text-${color} fa-7x`} />
            </h3>
            <h3 className={`text-center mt-3`}>
                {"Days to Trending: "}
                <span className={`text-${color}`}>
                    {data.prediction}
                </span>
            </h3>
        </div>
    )
}

export default Sentiment
