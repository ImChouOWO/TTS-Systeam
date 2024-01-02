import React, { useEffect, useRef } from 'react';
import { Application } from '@pixi/app';
import { Renderer } from '@pixi/core';
import { Ticker, TickerPlugin } from '@pixi/ticker';
import { InteractionManager } from '@pixi/interaction';
import { Live2DModel, MotionPreloadStrategy } from 'pixi-live2d-display';



function Live2DComponent({ parentRef }) {
  const canvasRef = useRef(null);
  
 
  useEffect(() => {
    // 注册必要的 PIXI 插件
    const { offsetWidth, offsetHeight } = parentRef.current;
    Live2DModel.registerTicker(Ticker);

    // 为 Application 注册 Ticker
    Application.registerPlugin(TickerPlugin);

    // 注册 InteractionManager 以支持 Live2D 模型的自动交互
    Renderer.registerPlugin('interaction', InteractionManager);

    const canvas = canvasRef.current;
    
    const app = new Application({
      backgroundAlpha: 0,
      view: canvas,
      width:offsetWidth,
      height: offsetHeight,
    });
    
    // 加载 Live2D 模型
    
    Live2DModel.from('/live2d/shizuku.model.json', {
        autoInteract: false,
        motionPreload: MotionPreloadStrategy.IDLE
      }).then(model => {
        // 确保 app 和 app.stage 存在
        if (app && app.stage) {
          app.stage.addChild(model);
      
          // 设置模型的初始位置和大小
          model.anchor.set(0.5, 0.5);
          model.scale.set(0.3, 0.3);
          model.position.set(offsetWidth/2, offsetHeight/1.5);
      
          // 添加交互逻辑
          canvas.addEventListener('pointerdown', (event) => {
            model.focus(event.clientX, event.clientY);
            model.tap(event.clientX, event.clientY);
          });
      
          canvas.addEventListener('pointermove', (event) => {
            if (event.buttons === 1) {
              model.focus(event.clientX, event.clientY);
            }
          });
        }
      });
      
  }, []);

  return <canvas className='live2dCanva' ref={canvasRef} />;
}

export default Live2DComponent;
